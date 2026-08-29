from collections import deque
from threading import Lock
from scapy.all import Packet

from ..meta_packet import MetaPacket
from scapy.contrib.modbus import *
from .transaction_manager import TransactionManager
from time import time

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ....app_core import Context

class ModbusBuffer:

    def __init__(self, context: "Context", max_size: int = 5000):
        self.context = context
        self.max_size = max_size

        self.singles_lock = Lock()
        self.commands_lock = Lock()

        self.stripchart_buffers = {}
        self.stripchart_locks = {}
        self.single_times = {}
        self.reset()

    def reset(self):
        with self.singles_lock:
            self.singles = {}
            self.commands = {}
        for var_name in self.context.states.get_registers():
            for dir in ["in", "out"]:
                key = f"{var_name}_{dir}"
                self.stripchart_buffers[key] = deque(maxlen=self.max_size)
                self.stripchart_locks[key] = Lock()
                self.singles[key] = None
                self.single_times[key] = time()
            self.commands[var_name] = None

    def put(self, mpkt: MetaPacket):
        # only one update/entry per useful (read response / write request) and primary (first to be put())
        packet_time = mpkt.get("time")
        is_primary = mpkt.get("is_primary")
        values = mpkt.get("values")
        variables = mpkt.get("variables")
        direction = mpkt.get("direction")
        useful = mpkt.get("is_useful")
        if not is_primary or not useful or len(values) < 1 or len(variables) < 1:
            return

        for i, var in enumerate(variables):
            key = f"{var}_{direction}"
            with self.stripchart_locks[key]:
                if len(self.stripchart_buffers[key]) > 0:
                # duplicate value to make a staircase shape
                    previous_value = self.stripchart_buffers[key][-1][1]
                    self.stripchart_buffers[key].append((packet_time - 0.0000001, previous_value))
                self.stripchart_buffers[key].append((packet_time, values[i]))
            with self.singles_lock:
                self.singles[key] = values[i]
                self.single_times[key] = time()
            with self.commands_lock:
                self.commands[var] = mpkt.get("command_word")

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

    def get_all_histories_and_legends(self, variable: str) -> dict[str, list[tuple[float, float]]]:
        '''
        Returns every exchange-type bucket's history for one register, keyed by
        exchange type ("in"/"out"/"A->B"/"B->A"/"other") - the key doubles as the
        strip chart's legend name for that line.
        '''
        return {direction: self.get_history(variable, direction) for direction in ["in", "out"]}