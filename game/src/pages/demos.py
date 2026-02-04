from ..widgets.common import Common as place
from ..widgets.map import Map
from customtkinter import CTkCanvas
from threading import Lock
from ..drawing.viewport import ViewPort
from ..network import network_controller

# from ..network import network_controller

class Demos:

    def triangle(root):

        def draw_test_plane(canvas: CTkCanvas, draw_lock: Lock, scale: float, offset: tuple[float, float]):
            draw = ViewPort(canvas, scale, offset)
            with draw_lock:
                canvas.delete("all")
                draw.test_triangle()

        world_map = Map(root, draw_test_plane, 100)

    def sprites(root):

        def draw_test_map(canvas: CTkCanvas, draw_lock: Lock, scale: float, offset: tuple[float, float]):
            draw = ViewPort(canvas, scale, offset)
            with draw_lock:
                canvas.delete("all")
                draw.ocean()
                draw.line([(0, 0), (200, 200)], "white")
                draw.boat((100,100), 0)
                draw.boat((100,100), 3.14/2)
                draw.boat((100,100), -3.14/4)
                draw.boat((0,0), -3.14/4)
                draw.boat((200,0), -3.14/4)
                draw.boat((0,200), -3.14/4)
                draw.boat((200,200), -3.14/4)

        world_map = Map(root, draw_test_map, 100)


    def net_map(root):

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
            draw = ViewPort(canvas, scale, offset)
            with draw_lock:
                canvas.delete("all")
                draw.grid_lines()
                if len(positions) < 1: return
                draw.poly_line(positions, "white")
                if bearing is None: return
                bearing = bearing[0]
                last_position = positions[-1]
                draw.boat(last_position, bearing, "white", "black")
        
        # Build page
        menu_bar = place.menu_bar(root, "Demo")
        
        no_button = place.menu_bar_button(menu_bar, "Start Printing")
        place.configure_reversible_button(no_button, lambda:print("start"), lambda:print("stop"), "Printing")
        
        attack_button = place.menu_bar_button(menu_bar, "Start Attack")
        place.configure_reversible_button(attack_button, start_attack, stop_attack, "Attack")

        left, middle, right = place.trifold(root)

        map = Map(middle, draw_full_map, 100, 20)

        return


    def saved_map(root):
        net = network_controller.SavedNetwork()

        def start_attack():
            net.start_arp()
            net.start_nfq()

        def stop_attack():
            net.stop_nfq()
            net.stop_arp()

        def draw_full_map(canvas: CTkCanvas, draw_lock: Lock, scale: float, offset: tuple[float, float]):
            positions = net.buffer.get_all_positions("in")
            bearing = net.buffer.get_last_tuple("theta", "in")
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
        
        # Build page
        menu_bar = place.menu_bar(root, "Demo")
        
        no_button = place.menu_bar_button(menu_bar, "Start Printing")
        place.configure_reversible_button(no_button, lambda:print("start"), lambda:print("stop"), "Printing")
        
        attack_button = place.menu_bar_button(menu_bar, "Start Attack")
        place.configure_reversible_button(attack_button, start_attack, stop_attack, "Attack")

        left, middle, right = place.trifold(root)

        map = Map(middle, draw_full_map, 100, 20)

        return