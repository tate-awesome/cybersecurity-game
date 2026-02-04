from ..widgets.common import Common as place
from ..widgets.map import Map
from ..drawing import sprites
from customtkinter import CTkCanvas
from threading import Lock

from ..network import network_controller

class Demos:

    def triangle(root):

        def draw_test_plane(canvas: CTkCanvas, draw_lock: Lock, scale: float, offset: tuple[float, float]):
            with draw_lock:
                canvas.delete("all")
                sprites.test_triangle(canvas, scale, offset)
        world_map = Map(root, draw_test_plane, 100)

    def map(root):

        # Create and define network control
        net = network_controller.HardwareNetwork()

        def start_attack():
            net.start_arp()
            net.start_nfq()

        def stop_attack():
            net.stop_nfq()
            net.stop_arp()

        def draw_full_map(canvas: CTkCanvas, draw_lock: Lock, scale: float, offset: tuple[float, float]):
            positions = net.buffer.get_all_positions("in")
            bearing = net.buffer.get_last_tuple("theta", "in")
            with draw_lock:
                canvas.delete("all")
                sprites.boat.grid_lines(canvas, scale, offset)
                if len(positions) < 1: return
                sprites.boat.poly_line(canvas, positions, scale, offset, "white")
                if bearing is None: return
                bearing = bearing[0]
                last_position = positions[-1]
                sprites.boat.boat(canvas, last_position, bearing, "white", "black", scale, offset)
        
        # Build page
        menu_bar = place.menu_bar(root, "Demo")
        
        no_button = place.menu_bar_button(menu_bar, "Start Printing")
        place.configure_reversible_button(no_button, lambda:print("start"), lambda:print("stop"), "Printing")
        
        attack_button = place.menu_bar_button(menu_bar, "Start Attack")
        place.configure_reversible_button(attack_button, start_attack, stop_attack, "Attack")

        left, middle, right = place.trifold(root)

        map = Map(middle, draw_full_map, 100, 20)


        return