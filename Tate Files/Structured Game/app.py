from Network.Hardware import arp_spoofing, sniffing, buffer, net_filter_queue, mod_table
from GUI.Drawing import map, sprites
import customtkinter as ctk
import GUI.Widgets.common as place
from threading import Lock
from math import pi as PI
from customtkinter import CTkCanvas


# Run as sudo for socket permissions?
# sudo python3 
# Password = veronica
# Be on GL-SFT1200-ab1 wifi
# Reset device before clicking start buttons
# ctrl+c in terminal to stop os commands - note: you shouldn't need to do this anymore
# trash terminal - note: you shouldn't need to do this anymore


# Wireshark filter:     ip.addr == 192.168.8.137 || arp



# root = ctk.CTk()
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()

# # root.geometry(f"{int(screen_width*3/4)}x{int(screen_height*3/4)}")
# root.attributes("-fullscreen", True)
# # root.state("iconic")
# root.title("Cybersecurity Game")

# nav_to_map(root)


# root.mainloop()


# test.converted_canvas()

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

def draw_test_plane(canvas: CTkCanvas, draw_lock: Lock, scale: float, offset: tuple[float, float]):
    with draw_lock:
        canvas.delete("all")
        sprites.test_triangle(canvas, scale, offset)

def draw_full_map(canvas: CTkCanvas, draw_lock: Lock, scale: float, offset: tuple[float, float]):
    positions = buffer.get_all_positions("in")
    bearing = buffer.get_last_tuple("theta", "in")
    with draw_lock:
        canvas.delete("all")
        sprites.boat.grid_lines(canvas, scale, offset)
        if len(positions) < 1: return
        sprites.boat.poly_line(canvas, positions, scale, offset, "white")
        if bearing is None: return
        last_position = positions[-1]
        # sprites.boat.boat(canvas, last_position, bearing, "white", "black")
        



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

    return



if __name__ == "__main__":
    root = ctk.CTk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.geometry(f"{int(screen_width*3/4)}x{int(screen_height*3/4)}")
    # root.attributes("-fullscreen", True)
    # root.state("iconic")
    root.title("Cybersecurity Game")
    def start():
        
        arp_spoofing.start()
        buffer.clear()
        # sniff.start(sniff.handlers.put_modbus_in_buffer)
        net_filter_queue.start(net_filter_queue.callbacks.buffer_and_accept)
        mod_table.set("speed", "offset", 5.0)
        mod_table.set("rudder", "mult", 0.0)
        

    def stop():
        net_filter_queue.stop()
        arp_spoofing.stop()
        mod_table.reset_table()
        

    place.big_button(root, "Start Hack", start)
    place.big_button(root, "Stop Hack", stop)
    
    world_map = map.Map(root, draw_test_plane, 100)

    root.mainloop()
