from netfilterqueue import NetfilterQueue as nfq
from scapy.all import *
from scapy.layers.inet import *
from scapy.utils import *
import scapy.contrib.modbus as mb
import re
import threading
import subprocess


import os

import random





def packet_listener(packet):
    
    
    pl=IP(packet.get_payload())

    #print('source IP:',pl[IP].src)
    #print('Destination IP', pl[IP].dst)
    #print('raw:',bytes(pl))

                 
                     
    
      
    pl.show()       
    send(pl)
    packet.accept()
           
           
            
           

    #print('plllllllllllllllllllllllll')

    

    #print(packet)
    
    #packet.accept()
  
     
  
  
def __setdown():
  os.system("sudo iptables -t mangle -D PREROUTING -i wlp0s20f3 -p TCP -j NFQUEUE --queue-num 1") 
    

os.system("sudo iptables -t mangle -A PREROUTING -i wlp0s20f3 -p TCP -j NFQUEUE --queue-num 1")
os.system("sudo iptables -L")
queue = nfq()

queue.bind(1, packet_listener)



try:
  print("Starting Attack")
  
  queue.run()
except KeyboardInterrupt:
  __setdown()
  print("stopping sniffing")
  queue.unbind()
