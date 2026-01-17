from queue import Queue


queue_size: int = 500


packet_queue = Queue(maxsize=queue_size)
number = 1

class PacketData():
    def __init__(self, pkt, modified: bool = False):
        self.pkt = pkt
        self.modified = modified

def pop() -> PacketData:
    try:
        return packet_queue.get_nowait()
    except:
        return 

def put(pkt, modified):
    p = PacketData(pkt, modified)
    try:
        packet_queue.put_nowait(p)
        return True
    except:
        # print("Buffer full")
        clear()
        return False

def clear():
    while not packet_queue.empty():
        packet_queue.get()

def size():
    return packet_queue.qsize()

# What does the GUI need?

'''
Name            key                                     purpose
Version         .version   "real" or "fake"             boat map        network map         wireshark
Source          .src                                                    network map         wireshark
Destination     .dst                                                    network map         wireshark
Variable        .var                                    boat map
Value           .val                                    boat map

No.             .no                                                                         wireshark
Transaction ID  .transId                                                                    wireshark
Time            .time                                                                       wireshark
Length          .len                                                                        wireshark
Info string     .info                                                                       wireshark

'''

# class PacketData:
#     def __init__(self, pkt, version):

#         self.version = version

#         self.source = pkt[IP].src
#         self.destination = pkt[IP].dst

#         if mb.is_x(pkt):
#             self.variable = "X"
#             self.values = [mb.get_coord(pkt)]
#         elif mb.is_y(pkt):
#             self.variable = "Y"
#             self.values = [mb.get_coord(pkt)]
#         elif mb.is_theta(pkt):
#             self.variable = "Theta"
#             self.values = [mb.get_coord(pkt)]
#         elif mb.is_commands(pkt):
#             self.variable = "Commands"
#             self.values = [mb.get_commands(pkt)]
#         else:
#             self.variable = "None"
#             self.values = ["None"]

#         self.transId = mb.get_transId(pkt)

#         self.number = buffer.number
#         buffer.number += 1
        
#         self.timestamp = time.time()
#         self.length = len(pkt[TCP].payload)
#         self.info = pkt.summary()
#         self.scannable = mb.print_scannable(pkt, print_to_console=False, convert=True)

