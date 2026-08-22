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
    # Every register gets a history bucket for each of these exchange types.
    # "in"/"out" are this host's own traffic; "A->B"/"B->A" track the one
    # sniffed third-party host pair this session has seen (see _other_direction);
    # "other" is a catch-all for anything not matching that pair (a third host,
    # broadcast, etc.).
    DIRECTIONS = ["in", "out", "A->B", "B->A", "other"]

    def __init__(self, context: "Context", max_size: int = 5000):
        self.context = context
        self.max_size = max_size

        self.singles_lock = Lock()
        self.commands_lock = Lock()

        self.stripchart_buffers = {}
        self.stripchart_locks = {}
        self.singles = {}
        self.single_times = {}
        self.commands = {}
        self.other_pair = None
        self.reset()

    def reset(self):
        self.other_pair = None
        for var_name in self.context.states.get_registers():
            for dir in self.DIRECTIONS:
                key = f"{var_name}_{dir}"
                self.stripchart_buffers[key] = deque(maxlen=self.max_size)
                self.stripchart_locks[key] = Lock()
                self.singles[key] = None
                self.single_times[key] = time()
            self.commands[var_name] = None

    def _other_direction(self, ip_src: str, ip_dst: str) -> str:
        '''
        Classifies one "other" (neither side is this host) packet as "A->B",
        "B->A", or the "other" catch-all. The first such packet seen since the
        last reset() fixes which host is "A" and which is "B" - this game's
        MITM/sniffing features (e.g. ARP spoofing) always target one victim/host
        pair at a time, so a single tracked pair covers the common case; traffic
        involving any other host falls into "other" instead of growing new buckets.
        '''
        if self.other_pair is None:
            self.other_pair = (ip_src, ip_dst)
        a, b = self.other_pair
        if ip_src == a and ip_dst == b:
            return "A->B"
        elif ip_src == b and ip_dst == a:
            return "B->A"
        else:
            return "other"

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

        if direction == "other":
            direction = self._other_direction(mpkt.get("ip_src"), mpkt.get("ip_dst"))

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
        return {direction: self.get_history(variable, direction) for direction in self.DIRECTIONS}