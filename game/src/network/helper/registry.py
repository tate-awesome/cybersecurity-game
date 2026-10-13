'''
The capabilities the privileged helper can host, by name.

This is the extension point: to move another privileged action into the
helper, add it here. Each factory returns an object with the same small
contract the GUI already uses for in-process actions - start(*args),
stop(), is_running() - taking (buffer, context) like network.process.Process.

Only runs inside the elevated helper process (see server.run), so importing
scapy and the hardware modules here is fine; the GUI side (host.py) never
imports this module.
'''
import time

from ..hardware.sniffing import Sniffer


def build_capability(name: str, buffer, context):
    if name == "sniff":
        return Sniffer(buffer, context)
    if name == "echo":
        return _Echo(buffer, context)
    raise KeyError(f"no helper capability named {name!r}")


class _Echo:
    '''
    A privilege-free self-test capability: on start it pushes a few
    synthetic packets and a status line through the buffer shim, so the
    whole helper path (launch, connection, serialization, from_payload) can
    be exercised offscreen without a real capture or elevation. Not used by
    the game itself.
    '''

    def __init__(self, buffer, context):
        self.buffer = buffer
        self._running = False

    def is_running(self) -> bool:
        return self._running

    def start(self, count: int = 3):
        from scapy.all import Ether, IP, TCP
        from scapy.contrib.modbus import ModbusADURequest, ModbusPDU03ReadHoldingRegistersRequest
        self._running = True
        packet = (Ether() / IP(src="192.168.4.2", dst="192.168.4.3") / TCP(sport=40000, dport=502)
                  / ModbusADURequest() / ModbusPDU03ReadHoldingRegistersRequest())
        packet.time = time.time()
        for _ in range(int(count)):
            self.buffer.put("sniff", "Sniffed Packet", packet, "in")
        self.buffer.put("sniff", "Echo capability done")
        self._running = False

    def stop(self):
        self._running = False
