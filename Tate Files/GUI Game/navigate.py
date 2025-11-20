import customtkinter as ctk
import os
import network_interface
import draw

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
            [     "Cycle Theme",          self.cycle_theme        ],
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
        place.menu_bar_button(menu_bar, "Cycle Theme", self.cycle_theme)

        # Place trifold
        left_pane, middle_pane, right_pane = place.trifold(self.root)

        # Place nmap button
        place.nmap_button(middle_pane, "Start probing network via NMap", print("nmaps"))
    
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
        place.menu_bar_button(menu_bar, "Cycle Theme", self.cycle_theme)

        # Place trifold
        left_pane, middle_pane, right_pane = place.trifold(self.root)

        # Place ip address form
        
    
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
        place.menu_bar_button(menu_bar, "Cycle Theme", self.cycle_theme)

        # Place trifold
        left_pane, middle_pane, right_pane = place.trifold(self.root)

        # Place nmap button
        place.nmap_button(middle_pane, "Start probing network via NMap", print("nmaps"))
    
    def cycle_theme(self):
        navigate = self.current_page
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
            self.clear(self.root)
            navigate()
            return
            
        theme_name = ctk.ThemeManager()._currently_loaded_theme

        if theme_name == "blue":
            theme = "themes/breeze.json"
        else:
            all_themes = os.listdir("themes")
            files = sorted([f for f in all_themes if os.path.isfile(os.path.join("themes", f))])
            i = files.index(theme_name.split('/')[1])
            if i >= len(files) - 1:
                theme = "blue"
            else:
                theme = "themes/"+files[i+1]

        ctk.ThemeManager.load_theme(theme)
        ctk.set_appearance_mode("Dark")
        self.clear(self.root)
        navigate()