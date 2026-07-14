from customtkinter import CTkFrame, CTkButton
from ...app_core.context import Context
from typing import Callable

class Overlay(CTkFrame):
    '''
    CTkFrame that is .place()'d below its trigger button on click. Is also .place_forget()'d when clicking outside the Overlay (this is expected behavior)
    '''

    def __init__(self, master, context: Context, button: CTkButton, populate_func: Callable[CTkFrame, None]):
        self.master = master
        self.context = context
        self.style = context.style
        self.button = button
        self.open_text = button._text
        self.manage_list()
        self.safe = False
        self.populate_func = populate_func
        super().__init__(self.master, border_color=self.style.color("accent"), border_width=2)

        # Set up
        self.click_close()
        def event_callback(event=None):
            self.click_close()
        self.context.root.bind("<Escape>", event_callback)
        self.context.click_manager.add_listener("overlay_click", self.click_handler)
        

    # Place / Unplace overlay

    def place_overlay(self):
        # Exit if already open
        if self.winfo_ismapped():
            return
        
        self.populate_func(self)
        self.update_idletasks()
        safe_x, safe_y = self.calculate_placement()
        
        self.place(x=safe_x, y=safe_y, anchor="nw")
        self.lift()

    def unplace_overlay(self):
        if self.winfo_ismapped():
            for child in self.winfo_children():
                child.destroy()
            self.place_forget()

    # Open/Close logic (clicking open button or clicking out to exit)

    def manage_list(self):
        if not hasattr(self.context, "overlay_list"):
            self.context.overlay_list = []
        if not self in self.context.overlay_list:
            self.context.overlay_list.append(self)

    def click_handler(self, event=None):
        print("\n\n\nclick")
        
        # 1. Force a single layout update before reading coordinates
        # self.context.root.update_idletasks()
        
        # Use a set to store overlays that are explicitly marked safe
        safe_overlays = set()
        visible_overlays = 0

        # 2. First Pass: Find who was clicked and mark their entire ancestry safe
        for overlay in list(self.context.overlay_list):
            if overlay.winfo_exists() and overlay.winfo_ismapped():
                visible_overlays += 1
                if overlay.click_checker(event):
                    # If this overlay was clicked, climb up its lineage and save all parents
                    widget = overlay
                    while widget is not None and isinstance(widget, Overlay):
                        safe_overlays.add(widget)
                        # Move to the button that spawned this overlay, then get its parent overlay
                        trigger_button = widget.get_button()
                        if trigger_button:
                            # Look up the tree to find the overlay containing the trigger button
                            widget = self._find_parent_overlay(trigger_button)
                        else:
                            widget = None
        if visible_overlays < 1:
            ...
        self.context.root.update_idletasks()
        # 3. Second Pass: Safely close anything NOT in the safe set
        for overlay in list(self.context.overlay_list):
            if overlay not in safe_overlays:
                overlay.click_close()

    def _find_parent_overlay(self, widget):
        """Helper to climb the Tkinter hierarchy to find the containing Overlay class"""
        current = widget
        while hasattr(current, "master") and current.master is not None:
            if isinstance(current.master, Overlay):
                return current.master
            current = current.master
        return None
        
        
    def click_checker(self, event=None):
        """
        Return True if the click is inside the overlay OR the trigger button.
        """
        if not self.winfo_exists() or not self.winfo_ismapped():
            return
        # 1. Check Overlay Bounding Box
        ox1 = self.winfo_rootx()
        oy1 = self.winfo_rooty()
        ox2 = ox1 + self.winfo_width()
        oy2 = oy1 + self.winfo_height()

        inside_overlay = (ox1 <= event.x_root <= ox2 and oy1 <= event.y_root <= oy2)

        # 2. Check Button Bounding Box
        button = self.get_button()
        if button and button.winfo_exists():
            bx1 = button.winfo_rootx()
            by1 = button.winfo_rooty()
            bx2 = bx1 + button.winfo_width()
            by2 = by1 + button.winfo_height()
            
            inside_button = (bx1 <= event.x_root <= bx2 and by1 <= event.y_root <= by2)
        else:
            inside_button = False
        print(f"{self} - overlay: {inside_overlay}. button: {inside_button}")
        # Return True if the click hit either area
        return inside_overlay or inside_button

    def click_close(self):
        self.configure_closed()
        self.unplace_overlay()

    def click_open(self):
        self.configure_opened()
        self.place_overlay()

    def configure_closed(self):
        if self.button._text == self.open_text and self.button._command == self.click_open:
            ...
        else:
            self.button.configure(command=self.click_open, text=self.open_text)
        if hasattr(self.button, "proxy") and self.button.proxy.winfo_exists():
            self.button.proxy.configure(command=self.click_open, text=self.open_text)

    def configure_opened(self):
        self.button.configure(command=self.click_close, text="Close")
        if hasattr(self.button, "proxy") and self.button.proxy.winfo_exists():
            self.button.proxy.configure(command=self.click_close, text="Close")

    # Placement helper

    def get_button(self):
        if hasattr(self.button, "proxy") and self.button.proxy.winfo_exists():
            active_button = self.button.proxy
        else:
            active_button = self.button
        return active_button
    
    def calculate_placement(self):
        # 1. Force initial layout update so button coordinates are accurate
        self.context.root.update_idletasks()
        
        # Scale correction factor
        scale = self.style.get_scale_correction()
        
        # Get current window boundaries
        win_w = self.context.root.winfo_width() / scale
        win_h = self.context.root.winfo_height() / scale

        active_button = self.get_button()
        
        # 2. Map coordinates relative to the top-left (NW) of the frame instead of center (N)
        # This aligns the math with your clipping constraints
        btn_left = (active_button.winfo_rootx() - self.context.root.winfo_rootx()) / scale
        btn_w = active_button.winfo_width() / scale
        btn_h = active_button.winfo_height() / scale
        igap = self.style.igap / scale

        # Ideal target: Center the overlay horizontally relative to the button
        # We will measure the actual width in the next step to offset this properly
        target_x = btn_left + (btn_w / 2)
        target_y = btn_left + btn_h + igap

        # 3. Temporarily place the frame out of view to force CustomTkinter to measure its true packed size
        self.place(x=-1000, y=-1000, anchor="nw")
        self.update_idletasks()
        
        # Now these dimensions are 100% accurate
        frame_w = self.winfo_width() / scale
        frame_h = self.winfo_height() / scale
        
        # 4. Calculate final X (Centered under button, but clamped within left/right window edges)
        # Start by shifting X left by half the frame width to achieve center-alignment
        safe_x = target_x - (frame_w / 2)
        safe_x = min(safe_x, win_w - frame_w) # Prevents right edge clipping
        safe_x = max(0, safe_x)               # Prevents left edge clipping
        
        # 5. Calculate final Y (Check if it clips the bottom, flip above button if it does)
        ideal_y_below = (active_button.winfo_rooty() - self.context.root.winfo_rooty()) / scale + btn_h + igap
        ideal_y_above = (active_button.winfo_rooty() - self.context.root.winfo_rooty()) / scale - frame_h - igap

        if ideal_y_below + frame_h > win_h:
            # If it clips the bottom edge, check if it fits above the button
            if ideal_y_above >= 0:
                safe_y = ideal_y_above # Fits perfectly above
            else:
                safe_y = max(0, win_h - frame_h) # Window is too small entirely; clamp to bottom edge
        else:
            safe_y = ideal_y_below # Fits perfectly below
        
        return safe_x, safe_y