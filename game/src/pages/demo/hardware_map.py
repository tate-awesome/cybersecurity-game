# TODO convert common object to style object and common module

'''
Unable to test
'''
from ...app_core.context import Context
from customtkinter import CTk


class HardwareMap:
    def __init__(self, context: Context):
        return
def net_map(root: CTk):

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