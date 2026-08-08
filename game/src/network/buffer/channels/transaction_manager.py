from ..meta_packet import MetaPacket
from scapy.contrib.modbus import *
from collections import OrderedDict

# I receive a request, modify it and pass it on
# I receive a response, modify it and pass it on

# The first request I see is what the master sent
# The last request I see is what the slave sees
# The first response I see is what the slave sent
# The last response I see is what the master sees

# I display the values I receive in yellow (reality to them)
# I display the values I send in pink (possibly altered)

# The write requests have the hreg and the value
# The read requests have the hreg
# The read responses have the values

class Transaction:

    def __init__(self):
        # The first one you get is good enough.
        # Sniffed in or preprocessing nfq
        # postprocessing nfq or sniffed out
        self.request_in = None      # Master -> MITM
        self.request_out = None     # MITM -> Slave
        self.response_in = None     # Slave -> MITM
        self.response_out = None    # MITM -> Master

        self.complete = False

        # The point of the commands is to tell the other party that a variable is something.
        # The type of command is the direction of the information
        # read holding registers request = what is x?
        # read holding registers response = x is this.      slave -> master
        # write holding registers request = x is this.
        # write holding registers response = ok.            master -> slave
    
    def add_mpkt(self, mpkt: MetaPacket):
        self._set_packet(mpkt)
        self._set_completeness()

    def enrich(self, mpkt: MetaPacket):
        '''
        (For read response usually) if there is a matching request, copy mpkt.variables to the mpkt parameter
        '''
        if mpkt.pkt.getlayer(ModbusADUResponse):
            if self.request_out is not None: # most accurate
                mpkt.variables = self.request_out.variables.copy()
            elif self.request_in is not None: #it will work
                mpkt.variables = self.request_in.variables.copy()
            mpkt.set_modbus_word()


    def _set_packet(self, mpkt: MetaPacket):
        if mpkt.pkt.getlayer(ModbusADURequest):
            if mpkt.direction == "in" and self.request_in is None:
                self.request_in = mpkt
            elif mpkt.direction == "out" and self.request_out is None:
                self.request_out = mpkt
        elif mpkt.pkt.getlayer(ModbusADUResponse):
            if mpkt.direction == "in" and self.response_in is None:
                self.response_in = mpkt
            elif mpkt.direction == "out" and self.response_out is None:
                self.response_out = mpkt

    def _set_completeness(self):
        if (self.request_out is not None and
                    self.request_in is not None and
                    self.response_out is not None and
                    self.response_in is not None):
            self.complete = True

class TransactionManager:
    def __init__(self):
        self.dict = OrderedDict()
        self.max_size = 20

    def enrich(self, mpkt: MetaPacket) -> None:
        transaction = self.try_add(mpkt)
        transaction.add_mpkt(mpkt)
        transaction.enrich(mpkt)

    def try_add(self, mpkt: MetaPacket) -> Transaction:
        '''
        Creates a new Transaction based on the MetaPacket's key.
        Adds it to the dict if it's a new key.
        Pops the oldest Transaction if the dict exceeds the max size.
        '''
        key = self.key(mpkt)
        if key in self.dict:
            return self.dict[key]
        self.dict[key] = Transaction()
        if len(self.dict) > self.max_size:
            self.dict.popitem(last=False)
        return self.dict[key]

    def clear(self):
        self.dict.clear()

    def contains(self, mpkt: MetaPacket):
        return self.key(mpkt) in self.dict

    def key(self, mpkt: MetaPacket):
        '''
        Returns a unique key for this modbus transaction:
        (client_ip, server_ip, transId)

        Requests: client -> server
        Response: server -> client
        '''
        if modbus_layer := mpkt.pkt.getlayer(ModbusADURequest):
            client_ip = mpkt.ip_src
            server_ip = mpkt.ip_dst
            tid = modbus_layer.transId
        elif modbus_layer := mpkt.pkt.getlayer(ModbusADUResponse):
            client_ip = mpkt.ip_dst
            server_ip = mpkt.ip_src
            tid = modbus_layer.transId
        else:
            return None
        return (client_ip, server_ip, tid)

    def get_command(self, mpkt: MetaPacket) -> tuple[list[str], list[float], str, str]:
        # example return: {register_2 = 44, register_3 = 91}, "in", "Read Response"
        direction = mpkt.direction
        command = ""

        
