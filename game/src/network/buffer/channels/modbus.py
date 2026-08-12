from collections import deque
from threading import Lock
from scapy.all import Packet

from ..meta_packet import MetaPacket
from scapy.contrib.modbus import *
from .transaction_manager import TransactionManager
from time import time

class ModbusBuffer:
    def __init__(self, context, max_size: int = 5000):
        self.context = context
        self.max_size = max_size

        self.singles_lock = Lock()
        self.commands_lock = Lock()
        
        self.slot_name = "modbus_variables"

        self.stripchart_buffers = {}
        self.stripchart_locks = {}
        self.singles = {}
        self.single_times = {}
        self.commands = {}
        self.reset()

    def reset(self):
        for var_name in self.context.states[self.slot_name]:
            for dir in ["in", "out"]:
                key = f"{var_name}_{dir}"
                self.stripchart_buffers[key] = deque(maxlen=self.max_size)
                self.stripchart_locks[key] = Lock()
                self.singles[key] = None
                self.single_times[key] = time()
            self.commands[var_name] = None

    def put(self, mpkt: MetaPacket):
        # only one update/entry per useful (read response / write request) and primary (first to be put())
        if not mpkt.is_modbus or len(mpkt.variables) < 1 or len(mpkt.variables) < 1 or not mpkt.is_useful_modbus or not mpkt.is_primary_modbus:
            return

        for i, var in enumerate(mpkt.variables):
            key = f"{var}_{mpkt.direction}"
            with self.stripchart_locks[key]:
                self.stripchart_buffers[key].append((mpkt.time, mpkt.values[i]))
            with self.singles_lock:
                self.singles[key] = mpkt.values[i]
                self.single_times[key] = time()
            with self.commands_lock:
                self.commands[var] = mpkt.command_word

        # TODO consider doing a dump so locks only engage once instead of 60 times
    def get_single(self, variable: str, direction: str) -> str:
        with self.singles_lock:
            value = self.singles[f"{variable}_{direction}"]
        return value

    def get_time(self, variable: str, direction: str) -> float:
        with self.singles_lock:
            value = self.single_times[f"{variable}_{direction}"]
        return value

    def get_command(self, variable: str) -> str:
        with self.commands_lock:
            value = self.commands[variable]
        return value

    def get_history(self, variable: str, direction: str):
        key = f"{variable}_{direction}"
        with self.stripchart_locks[key]:
            value = list(self.stripchart_buffers[key])
        return value