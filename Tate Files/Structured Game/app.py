from Network.Hardware import ARP_Spoofing as arp, Sniffing as sniff, Buffer as buffer
import customtkinter as ctk
import GUI.Widgets.common as place
import GUI.Drawing.map2 as draw
from threading import Lock


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

def draw_virtual_map(canvas, draw_lock):
    global points
    with draw_lock:
        canvas.delete("all")
        draw.triangle(canvas)

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
        arp.start()
        buffer.clear()
        sniff.start(sniff.handlers.put_modbus_in_buffer)

    def stop():
        sniff.stop()
        arp.stop()
        

    place.big_button(root, "Start Hack", start)
    place.big_button(root, "Stop Hack", stop)
    
    draw_lock = Lock()
    draw.zoom_pan_canvas(root, draw_virtual_map, 100, draw_lock)

    root.mainloop()
