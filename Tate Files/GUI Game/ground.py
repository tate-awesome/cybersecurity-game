import network_interface
from scapy.packet import Packet
from scapy.fields import ShortField, ByteField, FieldListField
from scapy.layers.inet import TCP
from scapy.all import bind_layers
from scapy.all import rdpcap
from scapy.contrib.modbus import *
# ModbusADURequest, ModbusADUResponse, ModbusPDU03ReadHoldingRegistersRequest

Net = network_interface.Network_Interface("saved")
print(Net.actual_boat_history)
        




# print(parent.keys()) #get attributes
# Net = network_interface.Network_Interface("virtual")