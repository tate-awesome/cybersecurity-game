from customtkinter import *

# Game window navigates by rebuilding the whole
# window
class Elements:
    def __init__(self):
        self.MED_FONT = CTkFont(family="Arial", size=16)
        self.DATA_FONT = CTkFont(family="Courier", size=16)
        self.HEADER_FONT = CTkFont(family="Arial", size=24)
        self.TITLE_FONT = CTkFont(family="Arial", size=max(32, self.root.winfo_height()//5), weight="bold")
        self.text_speed = 10
        self.tick_rate = 200
        self.OCEAN_COLOR = "#003459"
        return
    
    # packet handler (all info this packet)
        # access history for:
            # update canvas
            # pip network diagram
            # update packet spreadsheet
    
    # navigate to screen
        # check what's on
        # turn of unnecessary model stuff
        # turn on necessary model stuff
        # delete window content
        # build window
        # place element in (parent)
        
   
