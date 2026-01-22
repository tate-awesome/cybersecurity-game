import customtkinter as ctk
import GUI.Navigation.Demo_Pages.map as nav_to_map


# Run as sudo for socket permissions?
# sudo python3 
# Password = veronica
# Be on GL-SFT1200-ab1 wifi
# Reset device before clicking start buttons
# ctrl+c in terminal to stop os commands - note: you shouldn't need to do this anymore
# trash terminal - note: you shouldn't need to do this anymore


# Wireshark filter:     ip.addr == 192.168.8.137 || arp



root = ctk.CTk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# root.geometry(f"{int(screen_width*3/4)}x{int(screen_height*3/4)}")
root.attributes("-fullscreen", True)
# root.state("iconic")
root.title("Cybersecurity Game")

nav_to_map(root)


root.mainloop()


