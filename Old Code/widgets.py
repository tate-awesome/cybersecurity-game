import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import network
import math
import copy
import random
import network
from customtkinter import *
import csv
import time
import json
import re

global simplify_data
simplify_data = False

class Window:

    def __init__(self, ctk, app):
        super().__init__()
        # Game Objects: shared widgets
        self.ctk = ctk
        self.root = app

        # Game Flags: status with initial value
        self.theme = "blue.json"
        self.get_command_is_tweaked = False
        self.get_pos_is_tweaked = False
        self.packets_this_tick = 0
        self.packet_history = []
        self.pip_channels = []
        self.pos_history = []
        self.false_history = []
        self.rudder_history = []
        self.speed_history = []
        self.dir_history = []
        self.left_sidebar_hidden = False
        self.right_sidebar_hidden = True
        self.lying_position = []
        self.defend = False

        # Game Constants: useful constants 
        self.text_speed = 10
        self.tick_rate = 200
        self.OCEAN_COLOR = "#003459"
        self.help_message = "menu"
        self.help_messages = {
            "menu": "Welcome to Cybersecurity Game demo.\n\n\n"\
            "Click 'Play as Attacker' to start the demo.",

            "hacker_start": "Click the button to start probing\n"\
            "the network.",

            "hacker_ip": "Locate and enter the IP addresses for\n"\
            "the submarine and the submarine controller to start\n"\
            "sniffing for activity.",

            "hacker_encoding": "Enter a format to start\n"\
            "decoding the packets. 'utf-8' is a good idea.",

            "hacker_fields": "Find significant field names\n"\
            "in the decoded packets. If you track enough\n"\
            "fields, the packet stream can simulate the\n"\
            "submarine.",

            "hacker_hack": "Now start sending cyber attacks\n"\
            "to trick the submarine and controller. Expand the\n"\
            "right sidebar if you've closed it."

                        
            }

        # Popup messages
        self.ip_message = "Click Nmap to get your victim's ip address"

        # Game settings


        # App root
        
        # ⓘ



        # system_ip, controller_ip, network_recon_btn = pop.ip_pane(left_pane)

    def navigate_main_menu(self,):
        
        self.main_menu_frame = CTkFrame(self.root)
        self.main_menu_frame.pack(fill="both", expand=True)



        # Title

        # Title
        title_label = CTkLabel(
            self.main_menu_frame,
            text="Cybersecurity Game",
            font=self.TITLE_FONT
        )
        title_label.grid(row=1, column=1, ipady=20)



        # Buttons
        content_frame = CTkFrame(self.main_menu_frame, fg_color="transparent")
        content_frame.grid(row=2, column=1)

        defender_btn = CTkButton(content_frame, text="Play as Defender", width=240, height=40, command=self.open_defender_game, font=self.MED_FONT)
        defender_btn.pack(pady=10)

        hacker_btn = CTkButton(content_frame, text="Play as Attacker", width=240, height=40, command=self.start_hacker_game, font=self.MED_FONT)
        hacker_btn.pack(pady=10)

        help_btn = CTkButton(content_frame, text="Help", width=240, height=40, command=self.open_help_popup, font=self.MED_FONT)
        help_btn.pack(pady=10)

        settings_btn = CTkButton(content_frame, text="Settings", width=240, height=40, font=self.MED_FONT)
        settings_btn.pack(pady=10)

        theme_btn = CTkButton(content_frame, text="Cycle Theme", width=240, height=40, command=self.cycle_theme, font=self.MED_FONT)
        theme_btn.pack(pady=10)

        quit_btn = CTkButton(content_frame, text="Quit", width=240, height=40, command=self.root.destroy, font=self.MED_FONT)
        quit_btn.pack(pady=10)

        for i in [0, 3]:
            self.main_menu_frame.grid_rowconfigure(i, weight=1)
            self.main_menu_frame.grid_columnconfigure(i, weight=1)
        for i in [1, 2]:
            self.main_menu_frame.grid_rowconfigure(i, weight=0)
        
        self.main_menu_frame.grid_columnconfigure(1, weight=0)

        def resize(event):
            # scale font size with window width
            new_size = max(32, event.height // 20)
            title_label.configure(font=("Arial", new_size))

        self.main_menu_frame.bind("<Configure>", resize)


    def start_hacker_game(self):
        self.main_menu_frame.destroy()
        self.navigate_hacker()



    def open_help_popup(self):
        self.open_popup(self.root, self.help_messages[self.help_message])
    
    def cycle_theme(self):
        if self.ctk.get_appearance_mode() == "Dark":
            self.ctk.set_appearance_mode("Light")
            return
        else:
            self.ctk.set_appearance_mode("Dark")
        
        all_themes = os.listdir("themes")
        files = sorted([f for f in all_themes if os.path.isfile(os.path.join("themes", f))])
        if self.theme == "blue.json":
            self.theme = "breeze.json"
        else:
            i = files.index(self.theme)
            i = (i + 1)%len(files)
            self.theme = files[i]
        self.ctk.set_default_color_theme("themes/"+self.theme)
        
        self.root.winfo_children()[0].destroy()
        self.navigate_main_menu()
        
    def navigate_hacker(self):
        # Start boat in the background
        self.boat = network.Boat()
        self.boat.start()
        # Update help message
        self.help_message = "hacker_start"
        # Build window
        self.game_panes_frame = CTkFrame(master = self.root, fg_color="transparent")
        content = self.game_panes_frame
        content.pack(fill="both", expand=True)

        self.left_pane = CTkScrollableFrame(content, width=300)
        self.left_pane.grid(row=1, column=0, sticky="ns", padx=5, pady=5)
        # self.left_pane.grid_propagate()

        self.middle_pane = CTkFrame(content)
        self.middle_pane.grid(row=1, column=1, sticky="nsew", pady=5)

        self.right_pane = CTkFrame(content, width=300)
        # self.right_pane.grid(row=1, column=2, sticky="ns", padx=5, pady=5)
        self.right_pane.grid_propagate(False)

        menu_bar = CTkFrame(content)
        menu_bar.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=(5,0))

        self.game_label = CTkLabel(master = menu_bar, text="Cybersecurity Game: Hacker Mode", font=self.MED_FONT)
        self.game_label.pack(side="left", padx=20, pady=10)

        # theme_btn2 = CTkButton(menu_bar, text="Cycle Theme", width=200, height=40, command=self.cycle_theme)
        # theme_btn2.pack(pady=10)

        quit_btn = CTkButton(menu_bar, text="Quit", command=self.root.destroy, font=self.MED_FONT)
        quit_btn.pack(side="right", padx=10, pady=10)

        help_btn = CTkButton(menu_bar, text="Help", command=self.open_help_popup, font=self.MED_FONT)
        help_btn.pack(side="right", padx=10, pady=10)

        self.right_btn = CTkButton(menu_bar, text="Show Right Menu", command=self.toggle_right_sidebar, font=self.MED_FONT)
        self.right_btn.pack(side="right", padx=10, pady=10)

        self.left_btn = CTkButton(menu_bar, text="Hide Left Menu", command=self.toggle_left_sidebar, font=self.MED_FONT)
        self.left_btn.pack(side="right", padx=10, pady=10)

        content.grid_columnconfigure(0, weight=0)
        content.grid_columnconfigure(1, weight=1)
        content.grid_columnconfigure(2, weight=0)
        content.grid_rowconfigure(0, weight=0)
        content.grid_rowconfigure(1, weight=1)

        self.nmap_start_button = CTkButton(self.middle_pane, text="Start Probing Network via NMap", command=self.start_nmap, font=self.MED_FONT)
        self.nmap_start_button.grid(row=1, column=1, ipadx=20, ipady=10)
        
        for i in [0, 2]:
            self.middle_pane.grid_columnconfigure(i, weight=1)
            self.middle_pane.grid_rowconfigure(i, weight=1)
        self.middle_pane.grid_columnconfigure(1, weight=0)
        self.middle_pane.grid_rowconfigure(1, weight=0)
    
    def toggle_left_sidebar(self):
        if self.left_sidebar_hidden:
            self.left_btn.configure(text="Hide Left Menu")
            self.left_pane.grid(row=1, column=0, sticky="ns", padx=5, pady=5)
            self.left_sidebar_hidden = False
        else:
            self.left_btn.configure(text="Show Left Menu")
            self.left_pane.grid_forget()
            self.left_sidebar_hidden = True

    def toggle_right_sidebar(self):
        if self.right_sidebar_hidden:
            self.right_btn.configure(text="Hide Right Menu")
            self.right_pane.grid(row=1, column=2, sticky="ns", padx=5, pady=5)
            self.right_sidebar_hidden = False
        else:
            self.right_btn.configure(text="Show Right Menu")
            self.right_pane.grid_forget()
            self.right_sidebar_hidden = True

    def start_nmap(self):
        # Create dummy map
        self.nmap_start_button.destroy()
        self.navigate_nmap_results()
        self.navigate_ip_input()
    
    def navigate_nmap_results(self):
        # Update Help Message
        self.help_message = "hacker_ip"
        # Generate dummy nmap
        text = self.generate_nmap()
        random.shuffle(text)
        
        text = [["ip","state","hostname","mac","vendor"]] + text
        for row in text:
            if row[2] == "submarine":
                self.submarine_correct_ip = row[0]
            if row[2] == "submarine_controller":
                self.controller_correct_ip = row[0]
        

        self.nmap_frame = CTkFrame(self.middle_pane)

        content = self.nmap_frame
        content.pack(fill="both", expand=True)

        header = CTkLabel(content, text="NMap Results:", font=self.HEADER_FONT)
        header.pack(fill="x", side="top", anchor="w", padx=20, pady=10)
        spreadsheet = CTkScrollableFrame(content)
        spreadsheet.pack(fill="both", expand=True)
        

        for i in range(0, 9, 2):
            spreadsheet.grid_columnconfigure(i, weight=0)
        for i in range(1, 8, 2):
            spreadsheet.grid_columnconfigure(i, weight=1)

        def animate_nmap(ri):
            # Overload prevention
            if ri > 100:
                return
            try:
                next_row = text[ri]
            except:
                return
            for ci in range(0, len(text[ri])-1):
                word_box = CTkLabel(spreadsheet, text=text[ri][ci], font=self.DATA_FONT)
                word_box.grid(row=ri, column=ci*2, sticky="w", ipadx=10, ipady=5)
            spreadsheet.after(self.text_speed, lambda:animate_nmap(ri+1))
            return
        animate_nmap(0)
    
    def generate_nmap(self):
        text = self.read_csv_to_rows("nmap.csv")
        return text
    
    def read_csv_to_rows(self, path: str, encoding: str = "utf-8", has_header: bool = True):
        rows = []
        with open(path, newline="", encoding=encoding) as f:
            reader = csv.reader(f)
            if has_header:
                next(reader, None)  # skip header
            for row in reader:
                rows.append(row)
        return rows

    def navigate_ip_input(self):
        ip_frame = CTkFrame(self.left_pane)
        ip_frame.pack(side="top", fill="x", expand=False, padx=5, pady=5)
        ip_frame.columnconfigure(0, weight=0)
        ip_frame.columnconfigure(1, weight=1)
        ip_frame.columnconfigure(2, weight=0)

        ip_frame_header = CTkLabel(ip_frame, text="Device Addresses", font=self.HEADER_FONT)
        ip_frame_header.grid(row=0, column=0, columnspan="3", sticky="ew", pady=7, padx=10)

        system_ip_label = CTkLabel(ip_frame, text="System IP:", font=self.MED_FONT)
        system_ip_label.grid(row=1, column=1, sticky="w", pady=7, padx=10)
        self.system_ip_input = CTkEntry(ip_frame, font=self.MED_FONT)
        self.system_ip_input.grid(row=1, column=2, sticky="e", pady=7, padx=10)

        controller_ip_label = CTkLabel(ip_frame, text="Controller IP:", font=self.MED_FONT)
        controller_ip_label.grid(row=2, column=1, sticky="w", pady=7, padx=10)
        self.controller_ip_input = CTkEntry(ip_frame, font=self.MED_FONT)
        self.controller_ip_input.grid(row=2, column=2, sticky="e", pady=7, padx=10)

        # nmap_btn = tk.Button(ip_frame, text="Map Network")
        # nmap_btn.grid(row=2, column=1, sticky="w", pady=7, padx=10)
        self.network_sniffing_status = CTkLabel(ip_frame, text="", font=self.MED_FONT)
        self.network_sniffing_status.grid(row=3, column=1, sticky="w", pady=7, padx=10)

        self.network_sniffing_btn = CTkButton(ip_frame, text="Begin Sniffing", font=self.MED_FONT, command=self.try_network_sniffing)
        self.network_sniffing_btn.grid(row=3, column=2, sticky="e", pady=7, padx=10)
    
    def try_network_sniffing(self):
        if self.system_ip_input.get() != self.submarine_correct_ip and self.controller_ip_input.get() != self.controller_correct_ip:
            self.open_popup(self.root, "Error! Failed to locate system and controller IPs.\nPlease enter the correct system and controller IPs.")
            return
        if self.system_ip_input.get() != self.submarine_correct_ip:
            self.open_popup(self.root, "Error! Failed to locate system IP.\nPlease enter the correct system (submarine) IP.")
            return
        if self.controller_ip_input.get() != self.controller_correct_ip:
            self.open_popup(self.root, "Error! Failed to locate controller IP.\nPlease enter the correct controller IP.")
            return
        if self.system_ip_input.get() == self.submarine_correct_ip and self.controller_ip_input.get() == self.controller_correct_ip:
            self.network_sniffing_btn.configure(state="disabled")
            self.system_ip_input.configure(state="disabled")
            self.controller_ip_input.configure(state="disabled")
            # for i in range(0, 4):
            #     self.network_sniffing_status.after(i*1000, lambda i=i:self.network_sniffing_status.configure(text="Success!" + "."*i))
            # toffset = i*1000+2000
            # for j in range(0, 32):
                # self.network_sniffing_status.after(toffset+j*200, lambda j=j:rotating_animation(j))
            # toffset = toffset + j*200
            self.root.after(200, self.navigate_network_sniffing)
            
            # def rotating_animation(index):
            #     self.network_sniffing_status.configure(text="Loading "+"-\\|/-\\|/"[index%8])
            #     if index == 15:
            #         self.network_sniffing_status.configure(text="Sniffing...")

            # Testing section
            # self.network_listening_btn.configure(state="disabled")
            # self.system_ip_input.configure(state="disabled")
            # self.controller_ip_input.configure(state="disabled")
            # self.navigate_network_listening()

    def navigate_network_sniffing(self):
        
        self.help_message = "hacker_encoding"

        self.nmap_frame.destroy()
        print(self.middle_pane.winfo_children())

        self.network_frame = CTkFrame(self.middle_pane)
        content = self.network_frame
        content.pack(fill="both", expand=True)

        content.grid_columnconfigure(0, weight=1)   # single column stretches horizontally
        content.grid_rowconfigure(0, weight=1)      # top row grows/shrinks
        content.grid_rowconfigure(1, weight=0)      # bottom row fixed height

        self.network_stream_frame = CTkFrame(content)
        self.network_stream_frame.grid(row=0, column=0, sticky="nsew")

        self.network_model_frame = CTkFrame(content, height=200)
        self.network_model_frame.grid(row=1, column=0, sticky="nsew")
        
        self.navigate_network_binary_stream()
        self.navigate_decode_packets()
        self.navigate_network_diagram()

    def navigate_network_binary_stream(self):
        # Polls for new packets. Handles all events pertaining to new packet: adding packet entries, animation pips, adding to network tracking

        content = self.network_stream_frame

        header = CTkLabel(content, text="Packet Stream", font=self.HEADER_FONT)
        header.pack(fill="x", side="top", anchor="w", padx=20, pady=10)
        spreadsheet = CTkScrollableFrame(content)
        spreadsheet.pack(fill="both", expand=True)
        
        # Packets include:
        # No., Time, Source, Destination, Protocol, Length, Info (maybe not)
        headers = ["No.", "Time", "Source", "Destination", "Protocol", "Length"]
        numcols = len(headers)
        for i in range(0, numcols*2-1, 2):
            spreadsheet.grid_columnconfigure(i, weight=0)
        for i in range(1, numcols*2-2, 2):
            spreadsheet.grid_columnconfigure(i, weight=1)
        
        for i in range(0, len(headers)):
            word_box = CTkLabel(spreadsheet, text=headers[i], font=self.DATA_FONT)
            word_box.grid(row=0, column=i*2, sticky="w", ipadx=10, ipady=5)

        self.num_entries = 0

        def add_entry(packet):
            # Overload prevention
            if len(spreadsheet.winfo_children()) > 100:
                return
            self.num_entries += 1

            words = [str(self.num_entries),
                     time.ctime().split(" ")[3],
                     packet["source"],
                     packet["destination"],
                     "TCP",
                     str(len(json.dumps(packet["data"]))*8)
                     ]

            for i in range(0, len(words)):
                word_box = CTkLabel(spreadsheet, text=words[i], font=self.DATA_FONT)
                word_box.grid(row=self.num_entries, column=i*2, sticky="w", ipadx=10, ipady=5)

        def poll_for_packet():
            packet = dict()
            if self.boat.new_command_packet == True:
                try:
                    packet["source"] = self.controller_correct_ip
                    packet["destination"] = self.submarine_correct_ip
                    packet["data"] = self.boat.sub_command
                    self.boat.new_command_packet = False
                    add_entry(packet)
                    self.pip_network_diagram(packet["source"], packet["destination"])
                except Exception as e:
                    print(e)
                    return
            elif self.boat.new_pos_packet == True:
                try:
                    packet["source"] = self.submarine_correct_ip
                    packet["destination"] = self.controller_correct_ip
                    packet["data"] = self.boat.sub_pos
                    self.boat.new_pos_packet = False
                    add_entry(packet)
                    self.pip_network_diagram(packet["source"], packet["destination"])
                except Exception as e:
                    print(e)
                    return
            spreadsheet.after(self.tick_rate, poll_for_packet)
        poll_for_packet()
    
    def navigate_decode_packets(self):
        decode_packets_frame = CTkFrame(self.left_pane)
        decode_packets_frame.pack(side="top", fill="x", expand=False, padx=5, pady=5)

        decode_packets_header = CTkLabel(decode_packets_frame, text="Text Encoding", font=self.HEADER_FONT)
        decode_packets_header.pack(fill="x", pady=7, padx=10)

        input_frame = CTkFrame(decode_packets_frame)
        input_frame.pack()

        self.decode_field = CTkEntry(input_frame, font=self.MED_FONT)
        self.decode_field.pack(side="left", pady=7, padx=5)

        self.decode_button = CTkButton(input_frame, text="Decode Packets", font=self.MED_FONT, command=self.try_decode_packets)
        self.decode_button.pack(side="left", expand=False, pady=7, padx=5)
    
    def try_decode_packets(self):
        if self.decode_field.get() != "utf-8":
            self.open_popup(self.root, "Error! Failed to decode packets!\nTry using 'utf-8' to decode packets.")
            return
        if self.decode_field.get() == "utf-8":
            self.decode_field.configure(state="disabled")
            self.decode_button.configure(state="disabled")
            while len(self.network_stream_frame.winfo_children()) > 0:
                self.network_stream_frame.winfo_children()[0].destroy()
            self.navigate_network_plaintext_stream()
            self.navigate_track_fields()
        
    def navigate_network_plaintext_stream(self):
        # Polls for new packets. Handles all events pertaining to new packet: adding packet entries, animation pips, adding to network tracking
        self.fields = dict()
        content = self.network_stream_frame

        header = CTkLabel(content, text="Plaintext Packet Stream", font=self.HEADER_FONT)
        header.pack(fill="x", side="top", anchor="w", padx=20, pady=10)
        spreadsheet = CTkScrollableFrame(content)
        spreadsheet.pack(fill="both", expand=True)
        
        # Packets include:
        # No., Time, Source, Destination, Protocol, Length, Info (maybe not)
        headers = ["Body", "No.", "Time", "Source", "Destination", "Protocol", "Length"]
        numcols = len(headers)
        for i in range(0, numcols*2-1, 2):
            spreadsheet.grid_columnconfigure(i, weight=0)
        for i in range(1, numcols*2-2, 2):
            spreadsheet.grid_columnconfigure(i, weight=1)
        
        for i in range(0, len(headers)):
            word_box = CTkLabel(spreadsheet, text=headers[i], font=self.DATA_FONT)
            word_box.grid(row=0, column=i*2, sticky="w", ipadx=10, ipady=5)

        self.num_entries = 0

        def add_entry(packet):
            # Overload prevention 
            if len(spreadsheet.winfo_children()) > 100:
                return
            self.num_entries += 1


            words = [re.sub(r"\.\d+", "",json.dumps(packet["data"])),
                     str(self.num_entries),
                     time.ctime().split(" ")[3],
                     packet["source"],
                     packet["destination"],
                     "TCP",
                     str(len(json.dumps(packet["data"]))*8)
                     ]

            for i in range(0, len(words)):
                word_box = CTkLabel(spreadsheet, text=words[i], font=self.DATA_FONT)
                word_box.grid(row=self.num_entries, column=i*2, sticky="w", ipadx=10, ipady=5)

        def poll_for_packet():
            packet = dict()
            if self.boat.new_command_packet == True:
                try:
                    packet["source"] = self.controller_correct_ip
                    packet["destination"] = self.submarine_correct_ip
                    packet["data"] = self.boat.sub_command
                    self.boat.new_command_packet = False
                    data = packet["data"]
                    self.fields["speed"] = data["speed"]
                    self.fields["rudder"] = data["rudder"]
                    add_entry(packet)
                    self.pip_network_diagram(packet["source"], packet["destination"])
                except Exception as e:
                    print(e)
                    return
            elif self.boat.new_pos_packet == True:
                try:
                    packet["source"] = self.submarine_correct_ip
                    packet["destination"] = self.controller_correct_ip
                    packet["data"] = self.boat.sub_pos
                    self.boat.new_pos_packet = False
                    data = packet["data"]
                    self.fields["x"] = data["x"]
                    self.fields["y"] = data["y"]
                    self.fields["dir"] = data["dir"]
                    add_entry(packet)
                    self.pip_network_diagram(packet["source"], packet["destination"])
                except Exception as e:
                    print(e)
                    return
            spreadsheet.after(self.tick_rate, poll_for_packet)
        poll_for_packet()

    def navigate_track_fields(self):
        self.help_message = "hacker_fields"
        add_fields_frame = CTkFrame(self.left_pane)
        add_fields_frame.pack(side="top", fill="x", expand=False, padx=5, pady=5)

        fields_frame_header = CTkLabel(add_fields_frame, text="Add Fields to Track", font=self.HEADER_FONT)
        fields_frame_header.pack(fill="x", pady=7, padx=10)

        self.fields_grid = CTkLabel(add_fields_frame, anchor="w", font=self.DATA_FONT)
        self.fields_grid.pack(fill="x", pady=7, padx=10)

        new_field_frame = CTkFrame(add_fields_frame)
        new_field_frame.pack(side="top", fill="x", expand=False, padx=5)

        self.new_field_entry = CTkEntry(new_field_frame, font=self.MED_FONT)
        self.new_field_entry.pack(side="left", pady=7, padx=(0,20))

        self.new_field_button = CTkButton(new_field_frame, text="Add Field", font=self.MED_FONT, command=self.try_add_field)
        self.new_field_button.pack(side="right", pady=7)

        self.tracked_fields = []
        self.update_tracked_fields()
    
    def update_tracked_fields(self):
        message = []
        if self.tracked_fields.count("x") > 0:
            message.append(f"X Position:\t{math.floor(self.fields["x"]):05d}")

        if self.tracked_fields.count("y") > 0:
            message.append(f"Y Position:\t{math.floor(self.fields["y"]):05d}")

        if self.tracked_fields.count("dir") > 0:
            message.append(f"Bearing:   \t{math.floor(self.fields["dir"]):05d}")

        if self.tracked_fields.count("speed") > 0:
            message.append(f"Speed:     \t{math.floor(self.fields["speed"]):05d}")

        if self.tracked_fields.count("rudder") > 0:
            message.append(f"Rudder:    \t{math.floor(self.fields["rudder"]):05d}")

        # If we're tracking x and y, and the position is new, add it to history
        if self.tracked_fields.count("x") > 0 and self.tracked_fields.count("y") > 0:
            if len(self.pos_history) < 3:
                self.pos_history.append(self.fields["x"])
                self.pos_history.append(self.fields["y"])
            if self.pos_history[len(self.pos_history)-2] != self.fields["x"] or\
                self.pos_history[len(self.pos_history)-1] != self.fields["y"]:
                self.pos_history.append(self.fields["x"])
                self.pos_history.append(self.fields["y"])
            if len(self.false_history) < 3:
                self.false_history.append(self.boat.get_sub_pos()["x"])
                self.false_history.append(self.boat.get_sub_pos()["y"])
            if self.false_history[len(self.false_history)-2] != self.boat.get_sub_pos()["x"] or\
                self.false_history[len(self.false_history)-1] != self.boat.get_sub_pos()["y"]:
                self.false_history.append(self.boat.get_sub_pos()["x"])
                self.false_history.append(self.boat.get_sub_pos()["y"])
        # If we're tracking rudder, speed, dir, add them to their history
        if self.tracked_fields.count("rudder") > 0:
            self.rudder_history.append(self.fields["rudder"])
        if self.tracked_fields.count("speed") > 0:
            self.speed_history.append(self.fields["speed"])
        if self.tracked_fields.count("dir") > 0:
            self.dir_history.append(self.fields["dir"])
        self.fields_grid.configure(text="\n".join(message))
        self.fields_grid.after(200, self.update_tracked_fields)

    def try_add_field(self):
        new = self.new_field_entry.get()
        if new == "x" and self.tracked_fields.count("x") == 0:
            self.tracked_fields.append("x")
        elif new == "y" and self.tracked_fields.count("y") == 0:
            self.tracked_fields.append("y")
        elif new == "dir" and self.tracked_fields.count("dir") == 0:
            self.tracked_fields.append("dir")
        elif new == "speed" and self.tracked_fields.count("speed") == 0:
            self.tracked_fields.append("speed")
        elif new == "rudder" and self.tracked_fields.count("rudder") == 0:
            self.tracked_fields.append("rudder")
        else:
            self.open_popup(self.fields_grid, "Try adding a new field that appears in the packet bodies.")
        self.new_field_entry.delete(0,"end")
        if self.tracked_fields.count("x") > 0 and\
            self.tracked_fields.count("y") > 0 and\
            self.tracked_fields.count("dir") > 0 and\
            self.tracked_fields.count("speed") > 0 and\
            self.tracked_fields.count("rudder"):
            self.new_field_entry.configure(state="disabled")
            self.new_field_button.configure(state="disabled")
            self.navigate_network_video_stream()
            if self.defend == False:
                self.navigate_injection_panel()
            else:
                self.navigate_protection_panel()
            self.navigate_field_graphs()
        


    def open_popup(self, master, message):
        popup = self.ctk.CTkToplevel(master)
        popup.title("Help")
        popup.config(padx=10, pady=7)

        # Center to app
        width = 500
        height = 300
        root_x = master.winfo_rootx()
        root_y = master.winfo_rooty()
        win_x = root_x + master.winfo_width()/2 - width/2
        win_y = root_y + master.winfo_height()/2 - height/2

        popup.geometry(f"{width}x{height}+{int(win_x)}+{int(win_y)}")

        # Geometry

        # Add widgets to the popup
        frame = CTkFrame(popup)
        frame.pack(fill="both", side="top", padx=10, pady=7)

        label = CTkLabel(frame, text=message, font=self.MED_FONT)
        label.pack(pady=20, padx=10)

        close_button = CTkButton(frame, text="Dismiss", command=popup.destroy, font=self.MED_FONT)
        close_button.pack(pady=10, side="bottom")

        popup.grab_set()      # block interactions with main window
        popup.focus_force()   # force focus to the popup

    def navigate_field_graphs(self):
        field_graphs_frame = CTkFrame(self.left_pane)
        field_graphs_frame.pack(side="top", fill="x", expand=False, padx=5, pady=5)

        field_graphs_header = CTkLabel(field_graphs_frame, text="Fields Over Time", font=self.HEADER_FONT)
        field_graphs_header.pack(fill="x", pady=7, padx=10)

        speed_label = CTkLabel(field_graphs_frame, text="Speed", font=self.MED_FONT)
        speed_label.pack(side="top", fill="none", pady=15, padx=10)
        self.speed_graph = CTkCanvas(field_graphs_frame, height=100)
        self.speed_graph.pack(side="top", fill="x", pady=7, padx=5)

        dir_label = CTkLabel(field_graphs_frame, text="Direction", font=self.MED_FONT)
        dir_label.pack(side="top", fill="none", pady=15, padx=10)
        self.dir_graph = CTkCanvas(field_graphs_frame, height=100)
        self.dir_graph.pack(side="top", fill="x", pady=7, padx=5)

        rudder_label = CTkLabel(field_graphs_frame, text="Rudder", font=self.MED_FONT)
        rudder_label.pack(side="top", fill="none", pady=15, padx=10)
        self.rudder_graph = CTkCanvas(field_graphs_frame, height=100)
        self.rudder_graph.pack(side="top", fill="x", pady=7, padx=5)


    def navigate_network_video_stream(self):
        while len(self.network_stream_frame.winfo_children()) > 0:
            self.network_stream_frame.winfo_children()[0].destroy()
        # Polls for new packets. Handles all events pertaining to new packet: adding packet entries, animation pips, adding to network tracking
        content = self.network_stream_frame

        header = CTkLabel(content, text="System Simulation", font=self.HEADER_FONT)
        header.pack(fill="x", side="top", anchor="w", padx=20, pady=10)
        self.network_animate_canvas = CTkCanvas(content)
        self.network_animate_canvas.pack(fill="both", expand=True)

        self.network_video_animate()

        def poll_for_packet():
            packet = dict()
            if self.boat.new_command_packet == True:
                try:
                    packet["source"] = self.controller_correct_ip
                    packet["destination"] = self.submarine_correct_ip
                    packet["data"] = self.boat.sub_command
                    self.boat.new_command_packet = False
                    data = packet["data"]
                    self.fields["speed"] = data["speed"]
                    self.fields["rudder"] = data["rudder"]
                    self.pip_network_diagram(packet["source"], packet["destination"])
                except Exception as e:
                    print(e)
                    return
            elif self.boat.new_pos_packet == True:
                try:
                    packet["source"] = self.submarine_correct_ip
                    packet["destination"] = self.controller_correct_ip
                    packet["data"] = self.boat.sub_pos
                    self.boat.new_pos_packet = False
                    data = packet["data"]
                    self.fields["x"] = data["x"]
                    self.fields["y"] = data["y"]
                    self.fields["dir"] = data["dir"]
                    self.pip_network_diagram(packet["source"], packet["destination"])
                except Exception as e:
                    print(e)
                    return
            self.network_animate_canvas.after(self.tick_rate, poll_for_packet)
        poll_for_packet()
        return

    def network_video_animate(self):
        canvas = self.network_animate_canvas
        # Startup safety: re-run if there's not enough position history
        if len(self.pos_history) < 5:
            canvas.after(200, self.network_video_animate)
            return

        canvas.delete("all")
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        # We're pretty hard set on the 1000x1000 map
        x_target = self.boat.sub_target[0] * w/1000
        y_target = h - self.boat.sub_target[1] * h/1000

        tracks = []
        false_tracks = []
        i = 0
        for i in range(0, len(self.pos_history)-1):
            if i%2 == 0:
                tracks.append(self.pos_history[i] * w/1000)
            if i%2 == 1:
                tracks.append(h - self.pos_history[i] * h/1000)
            i += 1
        i = 0
        for i in range(0, len(self.false_history)-1):
            if i%2 == 0:
                false_tracks.append(self.false_history[i] * w/1000)
            if i%2 == 1:
                false_tracks.append(h - self.false_history[i] * h/1000)
            i += 1
        if len(tracks)%2 == 1:
            tracks.pop(len(tracks)-1)
        if len(false_tracks)%2 == 1:
            false_tracks.pop(len(false_tracks)-1)
        boat_vertices = [
                            [-2, 1],
                            [-2, -1],
                            [1, -1],
                            [3, 0],
                            [1, 1]
                            ]
        
        scale = h/60
        px = tracks[-4]
        py = tracks[-3]
        cx = tracks[-2]
        cy = tracks[-1]

        if len(false_tracks) < 4:
            false_tracks = tracks

        fpx = false_tracks[-4]
        fpy = false_tracks[-3]
        fcx = false_tracks[-2]
        fcy = false_tracks[-1]

        angle = math.atan2(py-cy, px-cx) + math.pi
        fangle = math.atan2(fpy-fcy, fpx-fcx) + math.pi

        real_vertices = []
        false_vertices = []

        for vx, vy in boat_vertices:
            x = vx * scale
            y = vy * scale

            fx = vx * scale
            fy = vy * scale

            xr = x * math.cos(angle) - y * math.sin(angle)
            yr = x * math.sin(angle) + y * math.cos(angle)

            fxr = fx * math.cos(fangle) - fy * math.sin(fangle)
            fyr = fx * math.sin(fangle) + fy * math.cos(fangle)

            xr += cx
            yr += cy

            fxr += fcx
            fyr += fcy

            real_vertices.extend([xr, yr])
            false_vertices.extend([fxr, fyr])

        canvas.create_rectangle(0, 0, w, h, fill=self.OCEAN_COLOR)
        canvas.create_line(false_tracks, width=2, fill="pink", dash=(15, 15))
        canvas.create_line(tracks, width=2, fill="white")

        canvas.create_polygon(false_vertices, fill="", outline="pink", outlinestipple="gray50")
        canvas.create_polygon(real_vertices, fill="dark gray", outline="black")

        canvas.create_line(x_target - 5, y_target, x_target + 5, y_target, width= 2, fill="red")
        canvas.create_line(x_target, y_target - 5, x_target, y_target + 5, width= 2, fill="red")

        # Graphing function
        def draw_history(c, h, min, max):
            if len(self.speed_history) < 4 or\
            len(self.dir_history) < 4 or\
            len(self.rudder_history) < 4:
                return
            print("Speed:"+str(int(self.speed_history[-1])))
            print("Rudder:"+str(int(self.rudder_history[-1])))
            print("Dir:"+str(int(self.dir_history[-1])))

            # Drawing program
            trace = []
            timescale = 10
            ch = c.winfo_height()
            cw = c.winfo_width()
            for i in range(0, len(h)-1):
                trace.append(cw - i*timescale)
                trace.append((1 - (h[-1-i] - min) / (max - min)) * ch)
            c.create_line(trace, width=4, fill="red")
            label_font = CTkFont(family="courier", size=24)
            c.create_text(1, 0, anchor="nw", text=str(max), font=label_font)
            c.create_text(1, (1-(0-min)/(max-min))*ch, anchor="w", text="0", font=label_font)
            c.create_text(1, ch, anchor="sw", text=str(min), font=label_font)
            c.create_text(cw-1, (1 - (h[-1] - min) / (max - min)) * ch, anchor="e", text=str(round(h[-1],2)), font=label_font)
            # Speed line
        try:
            #  CLEr GRAPHS -next step
            self.speed_graph.delete("all")
            self.rudder_graph.delete("all")
            self.dir_graph.delete("all")
            draw_history(self.speed_graph, self.speed_history, -20.0, 30.0)
            draw_history(self.dir_graph, self.dir_history, -180.0, 180.0)
            draw_history(self.rudder_graph, self.rudder_history, -20.0, 20.0)
        except:
            pass


        canvas.after(200, self.network_video_animate)

    def navigate_network_diagram(self):
        content = self.network_model_frame
        header = CTkLabel(content, text="Network Visualizer", font=self.HEADER_FONT)
        header.pack(fill="x", side="top", anchor="w", padx=20, pady=10)
        self.network_visual_canvas = CTkCanvas(content)
        self.network_visual_canvas.pack(fill="both", expand=True)
        self.network_visual_animate()

    def network_visual_animate(self):

        canvas = self.network_visual_canvas
        canvas.delete("all")
        w = canvas.winfo_width()
        h = canvas.winfo_height()

        canvas.create_rectangle(0,0,w,h,fill="#BEBEBE")

        
        self.packet_history.append(self.packets_this_tick)

        def draw_packet_history(c, vh, scale, centered):
            trace = []
            timescale = 10
            ch = c.winfo_height()
            cw = c.winfo_width()
            memory = 6
            if len(vh) < memory:
                return
            for i in range(memory, len(vh)-1):
                    trace.append(cw - (i-memory)*timescale)
                    running_peak = 0
                    for j in range(0, memory):
                        running_peak = max(running_peak, vh[j-i])
                    running_peak = running_peak
                    if centered:
                        trace.append(ch/2 - running_peak*scale-scale)
                    else:
                        trace.append(max(5, ch - running_peak*scale-scale))
            if len(trace) >= 4:
                c.create_line(trace, width=4, fill="red")
            label_font = CTkFont("Courier", 24, "bold")
            canvas.create_text(1, ch, anchor="sw", text="Packets per tick", font=label_font)
            canvas.create_text(1, ch-scale, anchor="w", text="0", font=label_font)
            canvas.create_text(1, ch-scale*2, anchor="w", text="1", font=label_font)
            canvas.create_text(1, ch-scale*3, anchor="w", text="2", font=label_font)
            canvas.create_text(1, ch-scale*4, anchor="w", text="3", font=label_font)
            canvas.create_text(1, ch-scale*5, anchor="w", text="4", font=label_font)
            canvas.create_text(1, ch-scale*6, anchor="w", text="5", font=label_font)
            canvas.create_text(1, ch-scale*7, anchor="w", text="6", font=label_font)
            canvas.create_text(1, ch-scale*8, anchor="w", text="7", font=label_font)


        draw_packet_history(canvas, self.packet_history, 40, False)
        
        server_height = canvas.winfo_height() * 0.8
        server_width = server_height*3/4
        server_margin = canvas.winfo_height() * 0.1
        # Wires:
        # Draw controller to submarine
        left_edge = server_margin + server_width
        right_edge = canvas.winfo_width() - server_margin - server_width
        middle = canvas.winfo_width()/2
        submarine_receive_height = canvas.winfo_height()/3
        controller_receive_height = canvas.winfo_height()*2/3

        canvas.create_line(left_edge, submarine_receive_height, right_edge, submarine_receive_height, fill="black", width=12)
        canvas.create_line(left_edge, controller_receive_height, right_edge, controller_receive_height, fill="black", width=12)

        
        def draw_controller_send():
            canvas.create_line(left_edge, submarine_receive_height, right_edge, submarine_receive_height, fill="yellow", width=8, arrow="last", arrowshape=(50,50,10))
        def draw_submarine_send():
            canvas.create_line(left_edge, controller_receive_height, right_edge, controller_receive_height, fill="yellow", width=8, arrow="first", arrowshape=(50,50,10))
        def draw_inject_to_controller():
            l = canvas.create_line(middle, controller_receive_height, left_edge, controller_receive_height, fill="red", width=8, arrow="last", arrowshape=(50,50,10))
            canvas.tag_raise(l)
        def draw_inject_to_submarine():
            l = canvas.create_line(middle, submarine_receive_height, right_edge, submarine_receive_height, fill="red", width=8, arrow="last", arrowshape=(50,50,10))
            canvas.tag_raise(l)

        for pip in self.pip_channels:
            if pip[0] == self.controller_correct_ip:
                draw_controller_send()
            if pip[0] == self.submarine_correct_ip:
                draw_submarine_send()
            if (pip[0] == "hacker" and pip[1] == self.controller_correct_ip) or self.get_pos_is_tweaked:
                draw_inject_to_controller()
            if (pip[0] == "hacker" and pip[1] == self.submarine_correct_ip) or self.get_command_is_tweaked:
                draw_inject_to_submarine()

        def draw_server(x_pos, y_pos, label):
            # Server body
            x = x_pos
            y = y_pos
            h = server_height
            w = server_width
            rack_margin = 10
            rack_height = 35
            canvas.create_rectangle(x, y, x+w, y+h, fill="#737373")
            # Top rack with text
            x = x + rack_margin
            w = w - rack_margin*2
            y = y + rack_margin
            h = rack_height
            canvas.create_rectangle(x, y, x+w, y+h, fill="#2D2D2D")
            canvas.create_text(x+w/2, y+2, anchor="n", text=label, fill="white", font=CTkFont("arial", 24, "bold"))
            # second rack with lights
            y = y + h + rack_margin
            canvas.create_rectangle(x, y, x+w, y+h, fill="#2D2D2D")
            canvas.create_line(x+rack_height/2, y+rack_height/2, x+w-rack_height/2, y+rack_height/2, dash=(30,30), width=3, fill="red")
            # Third rack
            y = y + h + rack_margin
            canvas.create_rectangle(x, y, x+w, y+h, fill="#2D2D2D")
            canvas.create_line(x+rack_height/2, y+rack_height/2, x+w-rack_height/2, y+rack_height/2, dash=(6,90), width=6, fill="white")
            # Fourth rack
            y = y + h + rack_margin
            canvas.create_rectangle(x, y, x+w, y+h, fill="#2D2D2D")
            canvas.create_line(x+rack_height/2, y+rack_height/2, x+w-rack_height/2, y+rack_height/2, dash=(20,150), width=3, fill="blue")
        
        draw_server(server_margin, server_margin, "Controller")
        draw_server(canvas.winfo_width()-server_width-server_margin, server_margin, "Submarine")
        draw_server(canvas.winfo_width()/2-server_width/2, server_margin, "You")
        self.packets_this_tick = 0
        self.pip_channels = []
        canvas.after(100, self.network_visual_animate)
    
    def pip_network_diagram(self, sender, receiver):
        self.packets_this_tick += 1
        self.pip_channels.append((sender, receiver))
        # print(self.pip_channels)
    
    def update_network_chart(self):
        return
    
    def navigate_injection_panel(self):
        self.help_message = "hacker_hack"
        injection_frame = CTkFrame(self.right_pane)
        injection_frame.pack(side="top", fill="both", expand=False, padx=5, pady=5)
        
        injection_frame_header = CTkLabel(injection_frame, text="Inject Packets", font=self.HEADER_FONT)
        injection_frame_header.pack(side="top", fill="x", expand=False, pady=7)

        tabs = CTkTabview(injection_frame)
        tabs.pack(side="top", fill="both", expand=True, padx=5, pady=5)

        clear_btn = CTkButton(injection_frame, text = "Clear Attacks", command=self.clear_attacks, font=self.MED_FONT)
        clear_btn.pack(side="left", padx=5, pady=7)

        ddos_btn = CTkButton(injection_frame, text = "Start DDoS Attack", font=self.MED_FONT)
        ddos_btn.pack(side="right", padx=5, pady=7)

        sub_tab = tabs.add("Send to Submarine")
        sub_desc = CTkLabel(sub_tab, text="Command the submarine's rudder and speed.\n"\
                                        "Alter the incoming command by X\n"\
                                        "or stream a new command altogether.",
                                        font=self.MED_FONT)
        sub_desc.pack(fill="x", pady=7)

        # Rudder section
        rudder_frame = CTkFrame(sub_tab)
        rudder_frame.pack(fill="x", pady=7)

        rudder_desc = CTkLabel(rudder_frame, text="Rudder", font=self.MED_FONT)
        rudder_desc.pack(side="left")

        self.rudder_alter = IntVar(value=1)
        rudder_alter = CTkCheckBox(rudder_frame, variable=self.rudder_alter, text="Alter", font=self.MED_FONT)
        rudder_alter.pack(side="right")

        self.rudder_entry = CTkEntry(rudder_frame)
        self.rudder_entry.pack(side="right", padx=10)
                
        # Speed section
        speed_frame = CTkFrame(sub_tab)
        speed_frame.pack(fill="x", pady=7)

        speed_desc = CTkLabel(speed_frame, text="Speed", font=self.MED_FONT)
        speed_desc.pack(side="left")

        self.speed_alter = IntVar(value=1)
        speed_alter = CTkCheckBox(speed_frame, variable=self.speed_alter, text="Alter", font=self.MED_FONT)
        speed_alter.pack(side="right")

        self.speed_entry = CTkEntry(speed_frame)
        self.speed_entry.pack(side="right", padx=10)


        send_sub = CTkButton(sub_tab, text="Send", command=self.send_sub)
        send_sub.pack(pady=7)

        cont_tab = tabs.add("Send to Controller")
        cont_desc = CTkLabel(cont_tab, text="Send position and direction data\n"
                                        "about the submarine to the controller.\n"\
                                        "Alter the outgoing data by X\n"\
                                        "or stream a constant value.",
                                        font=self.MED_FONT)
        cont_desc.pack(fill="x", pady=7)

        # X section
        x_frame = CTkFrame(cont_tab)
        x_frame.pack(fill="x", pady=7)

        x_desc = CTkLabel(x_frame, text="X", font=self.MED_FONT)
        x_desc.pack(side="left")

        self.x_alter = IntVar(value=1)
        x_alter = CTkCheckBox(x_frame, variable=self.x_alter, text="Alter", font=self.MED_FONT)
        x_alter.pack(side="right")

        self.x_entry = CTkEntry(x_frame)
        self.x_entry.pack(side="right", padx=10)

        # Y section
        y_frame = CTkFrame(cont_tab)
        y_frame.pack(fill="x", pady=7)

        y_desc = CTkLabel(y_frame, text="Y", font=self.MED_FONT)
        y_desc.pack(side="left")

        self.y_alter = IntVar(value=1)
        y_alter = CTkCheckBox(y_frame, variable=self.y_alter, text="Alter", font=self.MED_FONT)
        y_alter.pack(side="right")

        self.y_entry = CTkEntry(y_frame)
        self.y_entry.pack(side="right", padx=10)


        # Dir section
        dir_frame = CTkFrame(cont_tab)
        dir_frame.pack(fill="x", pady=7)

        dir_desc = CTkLabel(dir_frame, text="Direction", font=self.MED_FONT)
        dir_desc.pack(side="left")

        
        self.dir_alter = IntVar(value=1)
        dir_alter = CTkCheckBox(dir_frame, variable=self.dir_alter, text="Alter", font=self.MED_FONT)
        dir_alter.pack(side="right")

        self.dir_entry = CTkEntry(dir_frame)
        self.dir_entry.pack(side="right", padx=10)

        send_cont = CTkButton(cont_tab, text="Send", command=self.send_cont)
        send_cont.pack()
        

        


        # for attack in attacks:
        #     tabs.add(attack[0])
        #     attack_tab = tabs.tab(attack[0])
        #     sticky_redder_desc = CTkLabel(attack_tab, text=attack[1], font=self.MED_FONT)
        #     sticky_redder_desc.pack(side="top", fill="x", expand=False, padx=10, pady=7)
        #     sticky_rudder_button = CTkButton(attack_tab, text="Send Attack", command=attack[2], font=self.MED_FONT)
        #     sticky_rudder_button.pack(side="top", fill="none", padx=10, pady=7)
    def clear_attacks(self):
        def regular_get_command():
            return {"speed": self.boat.sub_command["speed"], "rudder": self.boat.sub_command["rudder"]}
        def regular_get_pos():
            return {"x": self.boat.sub_pos["x"], "y": self.boat.sub_pos["y"], "dir": self.boat.sub_pos["dir"]}
        self.get_command_is_tweaked = False
        self.get_pos_is_tweaked = False
        self.boat.get_command = regular_get_command
        self.boat.get_sub_pos = regular_get_pos

    def send_sub(self):
        try:
            change_speed = float(self.speed_entry.get())
        except:
            change_speed = 0
        try:
            change_rudder = float(self.rudder_entry.get())
        except:
            change_rudder = 0

        def evil_get_command():
            return {"speed": self.boat.sub_command["speed"] * self.speed_alter.get() + change_speed,
                    "rudder": self.boat.sub_command["rudder"] * self.rudder_alter.get() + change_rudder}
        self.boat.get_command = evil_get_command
        self.get_command_is_tweaked = True

    
    def send_cont(self):
        try:
            change_x = float(self.x_entry.get())
        except:
            change_x = 0
        try:
            change_y = float(self.y_entry.get())
        except:
            change_y = 0
        try:
            change_dir = float(self.dir_entry.get())
        except:
            change_dir = 0

        def evil_get_pos():
            return {"x": self.boat.sub_pos["x"] * self.x_alter.get() + change_x,
                    "y": self.boat.sub_pos["y"] * self.y_alter.get() + change_y,
                    "dir": self.boat.sub_pos["dir"] * self.dir_alter.get() + change_dir}
        self.boat.get_sub_pos = evil_get_pos
        self.get_pos_is_tweaked = True


    def open_defender_game(self):
        self.main_menu_frame.destroy()
        self.navigate_hacker()
        flag = True
        while flag:
            try:
                self.game_label.configure(text="Cybersecurity Game: Defender Mode")
                flag = False
            except:
                time.sleep(1)
        flag = True
        self.defend = True

    def navigate_protection_panel(self):
        self.help_message = "defender_defend"
        injection_frame = CTkFrame(self.right_pane)
        injection_frame.pack(side="top", fill="both", expand=False, padx=5, pady=5)
        
        injection_frame_header = CTkLabel(injection_frame, text="Encrypt", font=self.HEADER_FONT)
        injection_frame_header.pack(side="top", fill="x", expand=False, pady=7)

        tabs = CTkTabview(injection_frame)
        tabs.pack(side="top", fill="both", expand=True, padx=5, pady=5)

        clear_btn = CTkButton(injection_frame, text = "Filter Packets", command=self.clear_attacks, font=self.MED_FONT)
        clear_btn.pack(side="left", padx=5, pady=7)

        ddos_btn = CTkButton(injection_frame, text = "Limit Packet Rate", font=self.MED_FONT)
        ddos_btn.pack(side="right", padx=5, pady=7)

        sub_tab = tabs.add("Encrypt from Controller")
        sub_desc = CTkLabel(sub_tab, text="Encrypt data members.\n"\
                                        "\n"\
                                        "or stream a new command altogether.",
                                        font=self.MED_FONT)
        sub_desc.pack(fill="x", pady=7)

        # Rudder section
        rudder_frame = CTkFrame(sub_tab)
        rudder_frame.pack(fill="x", pady=7)

        rudder_desc = CTkLabel(rudder_frame, text="Rudder", font=self.MED_FONT)
        rudder_desc.pack(side="left")

        self.rudder_alter = IntVar(value=1)
        rudder_alter = CTkCheckBox(rudder_frame, variable=self.rudder_alter, text="Alter", font=self.MED_FONT)
        rudder_alter.pack(side="right")

        self.rudder_entry = CTkEntry(rudder_frame)
        self.rudder_entry.pack(side="right", padx=10)
                
        # Speed section
        speed_frame = CTkFrame(sub_tab)
        speed_frame.pack(fill="x", pady=7)

        speed_desc = CTkLabel(speed_frame, text="Speed", font=self.MED_FONT)
        speed_desc.pack(side="left")

        self.speed_alter = IntVar(value=1)
        speed_alter = CTkCheckBox(speed_frame, variable=self.speed_alter, text="Alter", font=self.MED_FONT)
        speed_alter.pack(side="right")

        self.speed_entry = CTkEntry(speed_frame)
        self.speed_entry.pack(side="right", padx=10)


        send_sub = CTkButton(sub_tab, text="Send", command=self.send_sub)
        send_sub.pack(pady=7)

        cont_tab = tabs.add("Encrypt from Submarine")
        cont_desc = CTkLabel(cont_tab, text="Encrypt data members\n"
                                        "about the submarine to the controller.\n"\
                                        "Alter the outgoing data by X\n"\
                                        "or stream a constant value.",
                                        font=self.MED_FONT)
        cont_desc.pack(fill="x", pady=7)

        # X section
        x_frame = CTkFrame(cont_tab)
        x_frame.pack(fill="x", pady=7)

        x_desc = CTkLabel(x_frame, text="X", font=self.MED_FONT)
        x_desc.pack(side="left")

        self.x_alter = IntVar(value=1)
        x_alter = CTkCheckBox(x_frame, variable=self.x_alter, text="Alter", font=self.MED_FONT)
        x_alter.pack(side="right")

        self.x_entry = CTkEntry(x_frame)
        self.x_entry.pack(side="right", padx=10)

        # Y section
        y_frame = CTkFrame(cont_tab)
        y_frame.pack(fill="x", pady=7)

        y_desc = CTkLabel(y_frame, text="Y", font=self.MED_FONT)
        y_desc.pack(side="left")

        self.y_alter = IntVar(value=1)
        y_alter = CTkCheckBox(y_frame, variable=self.y_alter, text="Alter", font=self.MED_FONT)
        y_alter.pack(side="right")

        self.y_entry = CTkEntry(y_frame)
        self.y_entry.pack(side="right", padx=10)


        # Dir section
        dir_frame = CTkFrame(cont_tab)
        dir_frame.pack(fill="x", pady=7)

        dir_desc = CTkLabel(dir_frame, text="Direction", font=self.MED_FONT)
        dir_desc.pack(side="left")

        
        self.dir_alter = IntVar(value=1)
        dir_alter = CTkCheckBox(dir_frame, variable=self.dir_alter, text="Alter", font=self.MED_FONT)
        dir_alter.pack(side="right")

        self.dir_entry = CTkEntry(dir_frame)
        self.dir_entry.pack(side="right", padx=10)

        send_cont = CTkButton(cont_tab, text="Send", command=self.send_cont)
        send_cont.pack()
    