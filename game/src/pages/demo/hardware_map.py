from ...network import network_controller
from ...drawing.viewport import ViewPort
from ...widgets.map import Map
from ...widgets import common as place
from ...widgets.style import Style
from ...app_core.context import Context


class HardwareMap:
    def __init__(self, context: Context):
        router, root = context.get_all()
        frame_ms = 100

        # Create and define network control
        net = network_controller.HardwareNetwork()
        context.net = net

        def start_attack():
            net.start_arp(target_ip='192.168.8.137', host_ip='192.168.8.243')
            net.start_nfq()

        def stop_attack():
            net.stop_nfq()
            net.stop_arp()

        def draw_full_map(canvas, draw_lock, scale: float, offset: tuple[float, float]):
            positions = net.buffer.get_all_positions("in")
            bearing = net.buffer.get_last_bearing("in")
            draw = ViewPort(canvas, scale, offset)
            with draw_lock:
                canvas.delete("all")
                draw.grid_lines()
                if len(positions) < 1: return
                draw.line(positions, "white")
                if bearing is None: return
                last_position = positions[-1]
                draw.boat(last_position, bearing, "white", "black")
        
        # Build page
        style = Style(context)
        menu_bar = place.menu_bar(style, root, "Demo")
        
        no_button = place.menu_bar_button(style, menu_bar, "Start Printing")
        place.configure_reversible_button(no_button, lambda:print("start"), lambda:print("stop"), "Printing")
        
        attack_button = place.menu_bar_button(style, menu_bar, "Start Attack")
        place.configure_reversible_button(attack_button, start_attack, stop_attack, "Attack")

        left, middle, right = place.trifold(style, root)

        map = Map(style, middle, draw_full_map, frame_ms, 20)

        return