from customtkinter import CTkFrame, CTkButton
from ...app_core.context import Context

class Overlay(CTkFrame):
    '''
    CTkFrame that is .place()'d below its trigger button on click. Is also .place_forget()'d when clicking outside the Overlay (this is expected behavior)
    '''
    def __init__(self, master, context: Context, button: CTkButton, open_text: str):
        self.master = master
        self.context = context
        self.style = context.style
        self.button = button
        self.open_text = open_text
        super().__init__(self.master, border_color=self.style.color("accent"), border_width=2)

        self.bind_overlay_button(button)


    def place_overlay(self):
        if self.winfo_ismapped():
            return
        
        # 1. Force initial layout update so button coordinates are accurate
        self.context.root.update_idletasks()
        
        # Scale correction factor
        scale = self.style.get_scale_correction()
        
        # Get current window boundaries
        win_w = self.context.root.winfo_width() / scale
        win_h = self.context.root.winfo_height() / scale
        
        # 2. Map coordinates relative to the top-left (NW) of the frame instead of center (N)
        # This aligns the math with your clipping constraints
        btn_left = (self.button.winfo_rootx() - self.context.root.winfo_rootx()) / scale
        btn_w = self.button.winfo_width() / scale
        btn_h = self.button.winfo_height() / scale
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
        ideal_y_below = (self.button.winfo_rooty() - self.context.root.winfo_rooty()) / scale + btn_h + igap
        ideal_y_above = (self.button.winfo_rooty() - self.context.root.winfo_rooty()) / scale - frame_h - igap

        if ideal_y_below + frame_h > win_h:
            # If it clips the bottom edge, check if it fits above the button
            if ideal_y_above >= 0:
                safe_y = ideal_y_above # Fits perfectly above
            else:
                safe_y = max(0, win_h - frame_h) # Window is too small entirely; clamp to bottom edge
        else:
            safe_y = ideal_y_below # Fits perfectly below

        # 6. Apply final calculated positions using anchor="nw"
        self.place(x=safe_x, y=safe_y, anchor="nw")
        self.lift()

    def unplace_overlay(self):
        if self.winfo_ismapped():
            self.place_forget()


    def bind_overlay_button(self, button: CTkButton):
        def configure_opened():
            button.configure(command=close, text=f"Close")
        def configure_closed():
            button.configure(command=open, text=self.open_text)
        def close():
            configure_closed()
            print("close")
            self.unplace_overlay()
        def open():
            configure_opened()
            self.place_overlay()
        def event_callback(event=None):
            close()
        self.context.root.bind("<Escape>", event_callback)
        configure_closed()