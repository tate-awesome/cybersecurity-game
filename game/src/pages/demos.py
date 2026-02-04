from ..widgets.common import Common as place
from ..widgets.map import Map
from ..drawing import sprites
from customtkinter import CTkCanvas
from threading import Lock
from ..drawing.viewport import ViewPort

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


    # def draw_test_map(canvas, draw_lock):
#     global points
#     with draw_lock:
#         canvas.delete("all")
#         # map.draw.test_triangle(canvas)
#         # path = buffer.flatten(buffer.get_knit_coordinates_in())
#         map.draw.ocean(canvas, "#003459")
#         map.draw.boat_path(canvas, (0, 0, 200, 200), "white")
#         map.draw.boat(canvas, [100,100], 0, "red", "")
#         map.draw.boat(canvas, [100,100], PI/2, "orange", "")
#         map.draw.boat(canvas, [100,100], -PI/4, "blue", "")
#         map.draw.boat(canvas, [0,0], -PI/4, "black", "white")
#         map.draw.boat(canvas, [200,0], -PI/4, "black", "white")
#         map.draw.boat(canvas, [0,200], -PI/4, "black", "white")
#         map.draw.boat(canvas, [200,200], -PI/4, "black", "white")
#         map.draw.coordinate_plane(canvas, 20)


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


        


    
# def draw_full_map(canvas, draw_lock):

#     path = buffer.get_flat_coordinates_in()
#     position = [buffer.get_last("x", "in"), buffer.get_last("y", "in")]
#     bearing = buffer.convert.theta_rad(buffer.get_last("theta", "in"))

#     with draw_lock:
#         canvas.delete("all")
#         map.draw.ocean(canvas, "#003459")
#         map.draw.coordinate_plane(canvas, 20)
#         map.draw.boat_path(canvas, path, "red")
#         map.draw.boat(canvas, position, bearing, "yellow", "yellow")



    # draw.ticks(canvas, [0, 0, 0, 1000], 100, 20, "white")
    # draw.ticks(canvas, [0, 0, 1000, 0], 100, 20, "white")

    # pos_history = buffer.get_knit_coordinates()
    # boat_pos = buffer.get_last_xyt()

    # # Draw fake path if available
    # if len(pos_history[1]) > 1:
    #     flat = [x for t in pos_history[1] for x in t]
    #     print(flat)
    #     draw.line(canvas, flat, "pink")

    # # Draw fake boat if available
    # if not (boat_pos[3] == None or boat_pos[4] == None or boat_pos[5] == None):
    #     x = boat_pos[3]
    #     y = boat_pos[4]
    #     dir = boat_pos[5]
    #     draw.boat(canvas, x, y, dir, "pink", "")
    #     print(x,"\t",y,"\t",dir)
    
    # # Draw real path if available
    # if len(pos_history[0]) > 1:
    #     flat = [x for t in pos_history[0] for x in t]
    #     draw.line(canvas, flat, "white")
    #     print(flat)


    # # Draw real boat if available
    # if not (boat_pos[0] == None or boat_pos[1] == None or boat_pos[2] == None):
    #     x = boat_pos[0]
    #     y = boat_pos[1]
    #     dir = boat_pos[2]
    #     print(x,"\t",y,"\t",dir)
    #     draw.boat(canvas, x, y, dir, "black", "white")


    
    
    # draw.target(canvas, net.target[0], net.target[1], "red")
    # draw.ticks(canvas, [x, y, net.target[0], net.target[1]], 10, 10, "green")
    # draw.ticks(canvas, pos_history[0], 10, 10, "black")

    # canvas.configure(scrollregion=canvas.bbox("all"))