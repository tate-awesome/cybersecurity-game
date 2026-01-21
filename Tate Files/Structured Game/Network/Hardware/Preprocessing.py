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