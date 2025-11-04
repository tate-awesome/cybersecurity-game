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
        self.current_nav = self.main_menu
    
    def clear(self, parent):
        while len(parent.winfo_children()) > 0:
            parent.winfo_children()[0].destroy()
    def clear_window(self):
        self.clear(self.root)
    
    def main_menu(self):
        self.clear(self.root)
        self.current_nav = self.main_menu
        menu_wrapper = place.main_menu.wrapper(self.root)
        place.main_menu.title(menu_wrapper, "Cybersecurity Game", self.root)
        buttons_wrapper = place.main_menu.buttons_wrapper(menu_wrapper)

        buttons = [
            [     "Play as Attacker",     self.hacker_start       ],
            [     "Play as Defender",     self.defender_start     ],
            [     "go to virtual map",    self.virtual_map],
            [     "Help",                 self.open_help_popup    ],
            [     "Cycle Theme",          self.cycle_theme     ],
            [     "Quit",                 self.quit_game          ]     ]

        for button in buttons:
            place.main_menu.button(buttons_wrapper, button[0], button[1])

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
            draw.ticks(canvas, [x, y, net.target[0], net.target[1]], 10, "green")
            draw.ticks(canvas, net.real_pos_history, 10, "black")
            draw.ticks(canvas, [0, 0, 0, 1000], 100, "white")
            draw.ticks(canvas, [0, 0, 1000, 0], 100, "white")
            return
        place.virtual_map.canvas(self.root, draw_virtual_map, 100)
        return

    def hacker_start(self):
        
        return
    def defender_start(self):
        return
    def open_help_popup(self):
        return
    
    def cycle_theme(self):
        navigate = self.current_nav
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
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
    
    def quit_game(self):
        return