import customtkinter as ctk
import os
import network_interface
import draw
from tkinter.filedialog import askopenfilename
import network_interface2 as net

import place
 # place element (parent)
        # place stuff there
        # tie button handlers to buttons
    # 
# place spreadsheet (parent, history, updater to be set)
    # 
class Navigate:
    def __init__(self, root):
        self.root = root
        self.current_page = self.main_menu
        place.set_fonts()
    
    def clear(self, parent):
        while len(parent.winfo_children()) > 0:
            parent.winfo_children()[0].destroy()
    def clear_window(self):
        self.clear(self.root)
    def quit_game(self):
        net.abort_all()
        self.root.destroy()
    def open_help_popup(self):
        return
    def open_settings(self):
        return
    
    def main_menu(self):
        self.clear(self.root)
        self.current_page = self.main_menu
        menu_wrapper = place.main_menu.wrapper(self.root)
        place.main_menu.title(menu_wrapper, "Cybersecurity Game", self.root)
        buttons_wrapper = place.main_menu.buttons_wrapper(menu_wrapper)

        buttons = [
            [     "Play as Attacker",     self.hacker_start       ],
            [     "Play as Defender",     self.defender_start     ],
            [     "go to virtual map",    self.virtual_map        ],
            [     "go to saved map",      self.saved_map        ],
            [     "Help",                 self.open_help_popup    ],
            [     "Settings",             self.open_settings      ],
            [     "Select Theme",          self.select_theme        ],
            [     "Quit",                 self.quit_game          ]     ]

        for button in buttons:
            place.main_menu.button(buttons_wrapper, button[0], button[1])

    # Virtual demo
    def virtual_map(self):
        self.clear_window()
        net = network_interface.Network_Interface("virtual")

        def draw_virtual_map(canvas):
            canvas.delete("all")
            draw.ocean(canvas, "#003459")
            if len(net.fake_pos_history) < 5 or len(net.real_pos_history) < 5:
                print(net.real_pos_history)
                return
            draw.line(canvas, net.fake_pos_history, "pink")
            x = net.fake_pos_history[-2]
            y = net.fake_pos_history[-1]
            dir = net.current_fake_direction
            draw.boat(canvas, x, y, dir, "pink", "")
            draw.line(canvas, net.real_pos_history, "white")
            x = net.real_pos_history[-2]
            y = net.real_pos_history[-1]
            dir = net.current_real_direction
            draw.boat(canvas, x, y, dir, "black", "white")
            draw.target(canvas, net.target[0], net.target[1], "red")
            draw.ticks(canvas, [x, y, net.target[0], net.target[1]], 10, 10, "green")
            draw.ticks(canvas, net.real_pos_history, 10, 10, "black")
            draw.ticks(canvas, [0, 0, 0, 1000], 100, 20, "white")
            draw.ticks(canvas, [0, 0, 1000, 0], 100, 20, "white")
            return
        place.virtual_map.canvas(self.root, draw_virtual_map, 100)
        return
    
    # Saved packets demo
    def saved_map(self):
        self.clear_window()
        net = network_interface.Network_Interface("saved")

        def draw_virtual_map(canvas):
            canvas.delete("all")
            draw.ocean(canvas, "#003459")
            draw.ticks(canvas, [0, 0, 0, 1000], 50, 2000, "grey")
            draw.ticks(canvas, [0, 0, 1000, 0], 50, 2000, "grey")
            if len(net.fake_pos_history) < 5 or len(net.real_pos_history) < 5:
                return
            draw.line(canvas, net.fake_pos_history, "pink")
            x = net.fake_pos_history[-2]
            y = net.fake_pos_history[-1]
            dir = net.current_fake_direction
            draw.boat(canvas, x, y, dir, "pink", "")
            draw.line(canvas, net.real_pos_history, "white")
            x = net.real_pos_history[-2]
            y = net.real_pos_history[-1]
            dir = net.current_real_direction
            draw.boat(canvas, x, y, dir, "black", "white")
            draw.target(canvas, net.target[0], net.target[1], "red")
            
            return
        place.virtual_map.canvas(self.root, draw_virtual_map, 100)
        return

# Hacker navigation
    def hacker_start(self):
        self.clear(self.root)
        self.current_page = self.hacker_start
        self.current_message = "hacker_start"

        # Place menu bar
        menu_bar = place.menu_bar(self.root, "Hacker Mode: Start Page")

        # Place menu buttons right to left
        place.menu_bar_button(menu_bar, "Quit", self.quit_game)
        place.menu_bar_button(menu_bar, "Help", self.open_help_popup)
        place.menu_bar_button(menu_bar, "Settings", self.open_settings)
        place.menu_bar_button(menu_bar, "Select Theme", self.select_theme)

        # Place trifold
        left_pane, middle_pane, right_pane = place.trifold(self.root)

        # Place nmap button
        place.big_button(middle_pane, "Start probing network via NMap", print("nmaps"))
    
    def hacker_nmap(self):
        self.clear(self.root)
        self.current_page = self.hacker_start
        self.current_message = "hacker_nmap"

        # Place menu bar
        menu_bar = place.menu_bar(self.root, "Hacker Mode: NMap Results")

        # Place menu buttons right to left
        place.menu_bar_button(menu_bar, "Quit", self.quit_game)
        place.menu_bar_button(menu_bar, "Help", self.open_help_popup)
        place.menu_bar_button(menu_bar, "Settings", self.open_settings)
        place.menu_bar_button(menu_bar, "Select Theme", self.select_theme)

        # Place trifold
        left_pane, middle_pane, right_pane = place.trifold(self.root)

        # Place ip address form

    def hacker_final(self):
        self.clear(self.root)
        self.current_page = self.hacker_final
        self.current_message = "hacker_final"

        # Place menu bar
        menu_bar = place.menu_bar(self.root, "Hacker Mode: Final Screen")

        # Place menu buttons right to left
        place.menu_bar_button(menu_bar, "Quit", self.quit_game)
        place.menu_bar_button(menu_bar, "Help", self.open_help_popup)
        place.menu_bar_button(menu_bar, "Settings", self.open_settings)
        place.menu_bar_button(menu_bar, "Select Theme", self.select_theme)

        # Place trifold
        left_pane, middle_pane, right_pane = place.trifold(self.root)
        
        # Place tabs
        middle_tabs = place.tab.container(middle_pane)
        pcap_tab = middle_tabs.add("pcap viewer")

        # Place tree
        columns = ("No.", "Time", "Source", "Destination", "Protocol", "Length Info")
        tree = place.tree.root(pcap_tab, columns)
        
        # Get unpacked pcap
        pcap_unpacked = network_interface.Network_Interface("pcap_viewer")

        # Place branches
        # tree.insert("", "end", values=(i, time, proto, pkt.summary()))

#Hacker hardware demo
    def hacker_hardware_demo(self):
        self.clear(self.root)
        self.current_page = self.hacker_hardware_demo
        self.current_message = "hacker_hardware_demo"

        # Place menu bar
        menu_bar = place.menu_bar(self.root, "Hacker Mode: Hardware Demo")

        # Place menu buttons right to left
        place.menu_bar_button(menu_bar, "Quit", self.quit_game)
        place.menu_bar_button(menu_bar, "Help", self.open_help_popup)
        place.menu_bar_button(menu_bar, "Settings", self.open_settings)
        place.menu_bar_button(menu_bar, "Select Theme", self.select_theme)

        # Place trifold
        left_pane, middle_pane, right_pane = place.trifold(self.root)
        
        # Place tabs
        # middle_tabs = place.tab.container(middle_pane)
        # pcap_tab = middle_tabs.add("pcap viewer")

        # Place tree
        # columns = ("No.", "Time", "Source", "Destination", "Protocol", "Length Info")
        # tree = place.tree.root(pcap_tab, columns)
        
        spoof_button = place.big_button(left_pane, "Start ARP Spoofing")
        def stop_spoof():
            spoof_button.configure(command=start_spoof, text="Stopping...")
            net.arp_spoofing.stop()
            spoof_button.configure(command=start_spoof, text="Start ARP Spoofing")

        def start_spoof():
            spoof_button.configure(command=start_spoof, text="Starting...")
            net.arp_spoofing.start()
            spoof_button.configure(command=stop_spoof, text="Stop ARP Spoofing")
        spoof_button.configure(command=start_spoof)

        sniff_button = place.big_button(left_pane, "Start Sniffing")
        def stop_sniff():
            sniff_button.configure(text="Stopping...")
            net.scapy_sniffing.stop()
            sniff_button.configure(command=start_sniff, text="Start Sniffing")
        def start_sniff():
            sniff_button.configure(text="Sniffing...")
            net.scapy_sniffing.start()
            sniff_button.configure(command=stop_sniff, text="Stop Sniffing")
        sniff_button.configure(command=start_sniff)

        nfq_button = place.big_button(left_pane, "Start Net Filter Queue")

        def stop_nfq():
            nfq_button.configure(text="Stopping...")
            net.mitm.stop()
            nfq_button.configure(command=start_nfq, text="Start Net Filter Queue")

        def start_nfq():
            nfq_button.configure(text="Queueing...")
            net.mitm.start()
            nfq_button.configure(command=stop_nfq, text="Stop Net Filter Queue")
        nfq_button.configure(command=start_nfq)

        queue_button = place.big_button(left_pane, "Print Packets to GUI")
        queue_print_running = False
        spreadsheet = place.big_textarea(middle_pane)

        def print_queue_line(textarea):
            try:
                place.append_text(textarea, net.buffer.pop().scannable)
            except:
                # print("error printing to GUI. buffer size = ", net.buffer.size())
                pass
            if queue_print_running:
                queue_button.after(5, lambda:print_queue_line(textarea))

        def start_printing_queue():
            print(net.config.to_string())
            nonlocal queue_print_running
            queue_print_running = True
            print_queue_line(spreadsheet)
            queue_button.configure(command=stop_printing_queue, text="Stop Printing")

        def stop_printing_queue():
            queue_button.configure(text="Stopping")
            nonlocal queue_print_running
            queue_print_running = False
            queue_button.configure(command=start_printing_queue, text="Print Packets to GUI")

        queue_button.configure(command=start_printing_queue)  
        
        queue_button.configure(command=start_printing_queue)


        xm, xo, x_button = place.form.double_entry(right_pane, "Multiplier", "offset", "Change X")
        ym, yo, y_button = place.form.double_entry(right_pane, "Multiplier", "offset", "Change Y")
        tm, to, t_button = place.form.double_entry(right_pane, "Multiplier", "offset", "Change Theta")
        sm, so, s_button = place.form.double_entry(right_pane, "Multiplier", "offset", "Change Speed")
        rm, ro, r_button = place.form.double_entry(right_pane, "Multiplier", "offset", "Change Rudder")
        
        xm.insert(0, "1.0")
        ym.insert(0, "1.0")
        tm.insert(0, "1.0")
        sm.insert(0, "1.0")
        rm.insert(0, "1.0")

        xo.insert(0, "0.0")
        yo.insert(0, "0.0")
        to.insert(0, "0.0")
        so.insert(0, "0.0")
        ro.insert(0, "0.0")

        def update_modifiers():
            net.mitm.xm = float(xm.get())
            net.mitm.ym = float(ym.get())
            net.mitm.tm = float(tm.get())
            net.mitm.sm = float(sm.get())
            net.mitm.rm = float(rm.get())

            net.mitm.xo = float(xo.get())
            net.mitm.yo = float(yo.get())
            net.mitm.to = float(to.get())
            net.mitm.so = float(so.get())
            net.mitm.ro = float(ro.get())

            print(net.config.to_string())
        
        x_button.configure(command=update_modifiers)
        y_button.configure(command=update_modifiers)
        t_button.configure(command=update_modifiers)
        s_button.configure(command=update_modifiers)
        r_button.configure(command=update_modifiers)

        # Place branches
        # tree.insert("", "end", values=(i, time, proto, pkt.summary()))

    
# Defender navigation
    def defender_start(self):
        self.clear(self.root)
        self.current_page = self.defender_start
        self.current_message = "defender_start"

        # Place menu bar
        menu_bar = place.menu_bar(self.root, "Defender Mode: Start Page")
        # Place menu buttons right to left
        place.menu_bar_button(menu_bar, "Quit", self.quit_game)
        place.menu_bar_button(menu_bar, "Help", self.open_help_popup)
        place.menu_bar_button(menu_bar, "Settings", self.open_settings)
        place.menu_bar_button(menu_bar, "Select Theme", self.select_theme)

        # Place trifold
        left_pane, middle_pane, right_pane = place.trifold(self.root)

        # Place nmap button
        place.big_button(middle_pane, "Start probing network via NMap", print("nmaps"))
    
    def select_theme(self):
        navigate = self.current_page
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
            self.clear(self.root)
            navigate()
            return
            
        # theme_name = ctk.ThemeManager()._currently_loaded_theme

        # if theme_name == "blue":
        #     theme = "themes/breeze.json"
        # else:
        #     all_themes = os.listdir("themes")
        #     files = sorted([f for f in all_themes if os.path.isfile(os.path.join("themes", f))])
        #     i = files.index(theme_name.split('/')[1])
        #     if i >= len(files) - 1:
        #         theme = "blue"
        #     else:
        #         theme = "themes/"+files[i+1]

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = askopenfilename(
            initialdir=f"{BASE_DIR}/themes",
            title="Select a file",
            filetypes=(("json", "*.json"),)
        )

        ctk.ThemeManager.load_theme(file_path)
        ctk.set_appearance_mode("Dark")
        self.clear(self.root)
        navigate()