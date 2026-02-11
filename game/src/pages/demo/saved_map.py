from ...widgets.map import Map
from ...app_core.context import Context
from customtkinter import CTkCanvas
from threading import Lock
from ...drawing.viewport import ViewPort
from ...widgets import common
from ...widgets.style import Style
from ...network import network_controller

class SavedMap:
    def __init__(self, context: Context):
        self.context = context
        self.context.net = network_controller.SavedNetwork()
        root = self.context.root
        
        # Build page
        style = Style(context.ui_scale)
        menu_bar = common.menu_bar(style, root, "Demo")
        
        attack_button = common.menu_bar_button(style, menu_bar, "Start Attack")
        common.configure_reversible_button(attack_button, self.start_attack, self.stop_attack, "Attack")

        left, middle, right = common.trifold(style, root)

        map = Map(style, middle, self.draw_full_map, 100, 20)


    def start_attack(self):
        self.context.net.start_arp()
        self.context.net.start_nfq()


    def stop_attack(self):
        self.context.net.stop_nfq()
        self.context.net.stop_arp()

    def draw_full_map(self, canvas: CTkCanvas, draw_lock: Lock, scale: float, offset: tuple[float, float]):
        positions = self.context.net.buffer.get_all_positions("in")
        bearing = self.context.net.buffer.get_last_tuple("theta", "in")
        draw = ViewPort(canvas, scale, offset)
        with draw_lock:
            canvas.delete("all")
            draw.grid_lines()
            if len(positions) < 1: return
            draw.line(positions, "black")
            if bearing is None: return
            bearing = bearing[0]
            last_position = positions[-1]
            draw.boat(last_position, bearing)