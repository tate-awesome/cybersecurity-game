from customtkinter import CTkFrame, CTkButton
from ...app_core import Context
from typing import Callable

class Overlay(CTkFrame):
    '''
    CTkFrame that is .place()'d below its trigger button on click. Is also .place_forget()'d when clicking outside the Overlay (this is expected behavior)
    '''

    def __init__(self, master, context: Context, button: CTkButton, populate_func: Callable[CTkFrame, None], anchor="south"):
        self.anchor = anchor
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
        safe_x, safe_y = self.calculate_placement(self.anchor)
        
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
        # print("\n\n\nclick")
        
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
        # print(f"{self} - overlay: {inside_overlay}. button: {inside_button}")
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
    
    def calculate_placement(self, anchor):
        # 1. Force initial layout update so button coordinates are accurate
        self.context.root.update_idletasks()

        # Scale correction factor
        scale = self.style.get_scale_correction()

        # Get current window boundaries
        win_w = self.context.root.winfo_width() / scale
        win_h = self.context.root.winfo_height() / scale

        active_button = self.get_button()

        # Button position relative to the root window
        btn_left = (
            active_button.winfo_rootx()
            - self.context.root.winfo_rootx()
        ) / scale

        btn_top = (
            active_button.winfo_rooty()
            - self.context.root.winfo_rooty()
        ) / scale

        btn_w = active_button.winfo_width() / scale
        btn_h = active_button.winfo_height() / scale
        igap = self.style.igap / scale

        # 3. Temporarily place the frame out of view to force
        # CustomTkinter to measure its true packed size
        self.place(x=-1000, y=-1000, anchor="nw")
        self.update_idletasks()

        frame_w = self.winfo_width() / scale
        frame_h = self.winfo_height() / scale

        # Button center points
        btn_center_x = btn_left + btn_w / 2
        btn_center_y = btn_top + btn_h / 2

        # ---------------------------------------------------------
        # NORTH: overlay below button
        # ---------------------------------------------------------
        if anchor == "south":
            safe_x = btn_center_x - frame_w / 2
            ideal_y = btn_top + btn_h + igap
            opposite_y = btn_top - frame_h - igap

            # Clamp X to window
            safe_x = min(safe_x, win_w - frame_w)
            safe_x = max(0, safe_x)

            # Prefer below, flip above if necessary
            if ideal_y + frame_h <= win_h:
                safe_y = ideal_y
            elif opposite_y >= 0:
                safe_y = opposite_y
            else:
                safe_y = max(0, win_h - frame_h)

        # ---------------------------------------------------------
        # SOUTH: overlay above button
        # ---------------------------------------------------------
        elif anchor == "north":
            safe_x = btn_center_x - frame_w / 2
            ideal_y = btn_top - frame_h - igap
            opposite_y = btn_top + btn_h + igap

            # Clamp X to window
            safe_x = min(safe_x, win_w - frame_w)
            safe_x = max(0, safe_x)

            # Prefer above, flip below if necessary
            if ideal_y >= 0:
                safe_y = ideal_y
            elif opposite_y + frame_h <= win_h:
                safe_y = opposite_y
            else:
                safe_y = max(0, min(ideal_y, win_h - frame_h))

        # ---------------------------------------------------------
        # EAST: overlay to right of button
        # ---------------------------------------------------------
        elif anchor == "east":
            safe_y = btn_center_y - frame_h / 2
            ideal_x = btn_left + btn_w + igap
            opposite_x = btn_left - frame_w - igap

            # Clamp Y to window
            safe_y = min(safe_y, win_h - frame_h)
            safe_y = max(0, safe_y)

            # Prefer right, flip left if necessary
            if ideal_x + frame_w <= win_w:
                safe_x = ideal_x
            elif opposite_x >= 0:
                safe_x = opposite_x
            else:
                safe_x = max(0, win_w - frame_w)

        # ---------------------------------------------------------
        # WEST: overlay to left of button
        # ---------------------------------------------------------
        elif anchor == "west":
            safe_y = btn_center_y - frame_h / 2
            ideal_x = btn_left - frame_w - igap
            opposite_x = btn_left + btn_w + igap

            # Clamp Y to window
            safe_y = min(safe_y, win_h - frame_h)
            safe_y = max(0, safe_y)

            # Prefer left, flip right if necessary
            if ideal_x >= 0:
                safe_x = ideal_x
            elif opposite_x + frame_w <= win_w:
                safe_x = opposite_x
            else:
                safe_x = max(0, min(ideal_x, win_w - frame_w))

        else:
            raise ValueError(
                f"Invalid anchor '{anchor}'. "
                "Expected 'north', 'south', 'east', or 'west'."
            )

        return safe_x, safe_y