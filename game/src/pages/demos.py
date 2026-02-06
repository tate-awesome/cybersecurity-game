from ..widgets.common import Common as place
from ..widgets.map import Map
from customtkinter import CTkCanvas, CTk
from threading import Lock
from ..drawing.viewport import ViewPort
from ..network import network_controller
from ..drawing import sprites, transformations as t
import time, random

# from ..network import network_controller

class Demos:

    def triangle(root: CTk):

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


    def saved_map(root: CTk):
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


    def boat_motion_map(root):
        
        # Make initial boat path
        positions = sprites.random_spline_path(20, 100)
        def random_visible_color():
            while True:
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)

                # Calculate brightness (perceived luminance)
                brightness = 0.299*r + 0.587*g + 0.114*b

                # White is ~255; reject colors that are too bright
                if brightness < 200:
                    return f"#{r:02x}{g:02x}{b:02x}"
        color = random_visible_color()


        def start_attack():
            positions = sprites.random_spline_path(20, 100)
            color = random_visible_color()


        def stop_attack():
            pass


        def draw_full_map(canvas: CTkCanvas, draw_lock: Lock, scale: float, offset: tuple[float, float]):
            path_duration = 30.0
            path_index = int(((time.time() % path_duration) / path_duration) * (len(positions)-2))
            bearing = t.get_bearing(positions[path_index], positions[path_index+1])
            draw = ViewPort(canvas, scale, offset)
            with draw_lock:
                canvas.delete("all")
                draw.grid_lines()
                draw.line(positions, color)
                last_position = positions[path_index]
                draw.boat(last_position, bearing)
        
        # Build page
        menu_bar = place.menu_bar(root, "Demo")
        
        no_button = place.menu_bar_button(menu_bar, "Start Printing")
        place.configure_reversible_button(no_button, lambda:print("start"), lambda:print("stop"), "Printing")
        
        attack_button = place.menu_bar_button(menu_bar, "Start Attack")
        place.configure_reversible_button(attack_button, start_attack, stop_attack, "Attack")

        left, middle, right = place.trifold(root)

        map = Map(middle, draw_full_map, 100, 20)