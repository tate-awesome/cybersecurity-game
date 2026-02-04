import GUI.Drawing.map as draw
import GUI.Widgets.common as place
import Network.Hardware.Buffer as buffer
import Network.Hardware.ARP_Spoofing as arp
import Network.Hardware.Net_Filter_Queue as nfq
import Network.Hardware.Sniffing as sniff
from customtkinter import CTkCanvas as can




import customtkinter as ctk


# Run as sudo for socket permissions?
# sudo python3 
# Password = veronica
# Be on GL-SFT1200-ab1 wifi
# Reset device before clicking start buttons
# ctrl+c in terminal to stop os commands - note: you shouldn't need to do this anymore
# trash terminal - note: you shouldn't need to do this anymore


# Wireshark filter:     ip.addr == 192.168.8.137 || arp

def static_map_hack():

    root = ctk.CTk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.geometry(f"{int(screen_width*3/4)}x{int(screen_height*3/4)}")
    # root.attributes("-fullscreen", True)
    # root.state("iconic")
    root.title("Cybersecurity Game")
    def start():
        arp.start()
        nfq.start(nfq.callbacks.buffer_and_modify)

    def stop():
        nfq.stop()
        buffer.clear()
        arp.stop()
        

    place.big_button(root, "Start Hack", start)
    place.big_button(root, "Stop Hack", stop)

    def draw_virtual_map(canvas):
        canvas.delete("all")
        draw.ocean(canvas, "#003459")

        draw.ticks(canvas, [0, 0, 0, 1000], 100, 20, "white")
        draw.ticks(canvas, [0, 0, 1000, 0], 100, 20, "white")

        pos_history = buffer.get_knit_coordinates()
        boat_pos = buffer.get_last_xyt()

        # Draw fake path if available
        if len(pos_history[1]) > 1:
            flat = [x for t in pos_history[1] for x in t]
            print(flat)
            draw.line(canvas, flat, "pink")

        # Draw fake boat if available
        if not (boat_pos[3] == None or boat_pos[4] == None or boat_pos[5] == None):
            x = boat_pos[3]
            y = boat_pos[4]
            dir = boat_pos[5]
            draw.boat(canvas, x, y, dir, "pink", "")
            print(x,"\t",y,"\t",dir)
        
        # Draw real path if available
        if len(pos_history[0]) > 1:
            flat = [x for t in pos_history[0] for x in t]
            draw.line(canvas, flat, "white")
            print(flat)


        # Draw real boat if available
        if not (boat_pos[0] == None or boat_pos[1] == None or boat_pos[2] == None):
            x = boat_pos[0]
            y = boat_pos[1]
            dir = boat_pos[2]
            print(x,"\t",y,"\t",dir)
            draw.boat(canvas, x, y, dir, "black", "white")


        
        
        # draw.target(canvas, net.target[0], net.target[1], "red")
        # draw.ticks(canvas, [x, y, net.target[0], net.target[1]], 10, 10, "green")
        # draw.ticks(canvas, pos_history[0], 10, 10, "black")
        return

    place.virtual_map.canvas(root, draw_virtual_map, 100)





    root.mainloop()


def dynamic_canvas():
    root = ctk.CTk()
    sw = int(root.winfo_screenwidth()*3/4)
    sh = int(root.winfo_screenheight()*3/4)
    root.geometry(f"{sw}x{sh}")

    root.title("Rectangle")
    def callback(canvas, cx, cy):
        canvas.delete("all")
        w = canvas.winfo_width()
        h = canvas.winfo_height()

        if cx == 0 and cy == 0:
            cx = cx + 10
        elif cx == 0 and cy == h:
            cy = cy - 10
        elif cx == w and cy == h:
            cx = cx - 10
        elif cx == w and cy == 0:
            cy = cy + 10

        elif cx == 0:
            cy = cy - 10
        elif cx == w:
            cy = cy + 10
        elif cy == 0:
            cx = cx + 10
        elif cy == h:
            cx = cx - 10
        


        canvas.create_rectangle(0, 0, cx, cy, fill="red", outline="black")
        return cx, cy
    place.virtual_map.zoom_pan_canvas(root, callback, 20)

    root.mainloop()



def converted_canvas():

    root = ctk.CTk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.geometry(f"{int(screen_width*3/4)}x{int(screen_height*3/4)}")
    # root.attributes("-fullscreen", True)
    # root.state("iconic")
    root.title("Cybersecurity Game")
    def start():
        arp.start()
        nfq.start(nfq.callbacks.buffer_and_modify)

    def stop():
        nfq.stop()
        buffer.clear()
        arp.stop()
        

    place.big_button(root, "Start Hack", start)
    place.big_button(root, "Stop Hack", stop)

    def draw_virtual_map(canvas: can):
        canvas.delete("all")
        draw.ocean(canvas, "#003459")

        draw.ticks(canvas, [0, 0, 0, 1000], 50, 20, "white")
        draw.ticks(canvas, [0, 0, 1000, 0], 50, 20, "white")

        pos_history = buffer.get_knit_coordinates()
        boat_pos = buffer.get_last_xyt()

        w = canvas.winfo_width()
        h = canvas.winfo_height()


        # Draw fake path if available
        if len(pos_history[1]) > 1:
            flat = [x for t in pos_history[1] for x in t]
            print(flat)
            converted = draw.range_transform(flat, 200, 200, w, h)
            draw.line(canvas, converted, "pink")

        # Draw fake boat if available
        if not (boat_pos[3] == None or boat_pos[4] == None or boat_pos[5] == None):
            x = boat_pos[3]
            y = boat_pos[4]
            dir = boat_pos[5]
            draw.boat(canvas, x, y, dir, "pink", "")
            print(x,"\t",y,"\t",dir)
        
        # Draw real path if available
        if len(pos_history[0]) > 1:
            flat = [x for t in pos_history[0] for x in t]
            draw.line(canvas, flat, "white")
            print(flat)


        # Draw real boat if available
        if not (boat_pos[0] == None or boat_pos[1] == None or boat_pos[2] == None):
            x = boat_pos[0]
            y = boat_pos[1]
            dir = boat_pos[2]
            print(x,"\t",y,"\t",dir)
            draw.boat(canvas, x, y, dir, "black", "white")


        
        return

    place.virtual_map.canvas(root, draw_virtual_map, 100)





    root.mainloop()