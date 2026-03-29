from ...app_core.context import Context
from ...network.meta_packet import MetaPacket
from ...network.data_buffer import DataBuffer
from customtkinter import *
from tkinter import ttk
import tkinter as tk

class Console:
    '''
    Wireshark-like treeview output for different hacks
    '''

    def __init__(self, style, parent, context: Context, buffer: DataBuffer):
        self.context = context
        self.style = style
        self.frame = parent
        self.buffer = buffer
        self.filter_func = lambda mpkt: True

        menu_frame = self.create_menu_frame(self.frame)
        refresh_button = self.create_menu_button(menu_frame, "Refresh")
        filter_button = self.create_menu_button(menu_frame, "Filters")
        self.bind_overlay_button(filter_button, self.create_filter_overlay, self.destroy_filter_overlay)

        # Designate menu filters


        # Create treeview
    
    # Menu
    def create_menu_frame(self, parent):
        menu_frame = CTkFrame(parent)
        menu_frame.pack(side="top", padx=self.style.gap, pady=self.style.gaptop, fill="x", anchor="n")
        return menu_frame
    
    def create_menu_button(self, frame, text, function=None):
        med = self.style.get_font()
        button = CTkButton(frame, text=text, command=function, font=med)
        button.pack(side="left", padx=self.style.gap, pady=self.style.gap)
        return button
    
    # Filter overlay
    def add_filter_options(self, parent: CTkFrame):
        '''
        Create filter menu widgets, load filter options from context and configure inputs for autosave
        '''
        # Create box filter widgets
        box_slots = self.context.inputs["checkbox_filters"]
        med = self.style.get_font()
        checkbox_frame = CTkFrame(parent)
        checkbox_frame.pack(side="top", padx=self.style.gap, pady=self.style.gaptop)

        for category in box_slots:

            category_frame = CTkFrame(checkbox_frame)
            category_frame.pack(side="left", anchor="n")
            category_label = CTkLabel(category_frame, text=category, font=med)
            category_label.pack(side="top", padx=self.style.gap, anchor="n")

            for box_name in box_slots[category]:

                filter_box = CTkCheckBox(category_frame, text=box_name, font=med)
                filter_box.pack(side="top", anchor="w", pady=self.style.gap, padx=self.style.gap)
                # Load previous input
                value = box_slots[category][box_name]["state"]
                if value == "1": filter_box.select()
                else: filter_box.deselect()
                # Configure for autosave
                def autosave(slot=box_slots[category][box_name], b=filter_box):
                    slot["state"] = str(b.get())
                filter_box.configure(command=autosave)
        

        # Create text filter widgets
        text_slots = self.context.inputs["text_filters"]
        entry_frame = CTkFrame(parent)
        entry_frame.pack(side="top", fill="x", padx=self.style.gap, pady=self.style.gap)

        for text_slot in text_slots:

            filter_label = CTkLabel(entry_frame, text=text_slots[text_slot]["label"], font=med)
            filter_label.pack(side="top", padx=self.style.gap, pady=self.style.gaptop)
            filter_entry = CTkEntry(entry_frame, font=med)
            filter_entry.pack(fill="x", side="top", padx=self.style.gap, pady=self.style.gap)
            # Load previous input
            previous_text = text_slots[text_slot]["text"]
            filter_entry.delete(0, "end")
            filter_entry.insert(0, previous_text)
            # Configure for autosave
            def autosave(event=None, e=filter_entry, slot=text_slots[text_slot]):
                slot["text"] = e.get()
            filter_entry.bind("<KeyRelease>", autosave)
        

    def create_filter_overlay(self, button: CTkButton):

        # Place overlay just below button
        x = button.winfo_rootx() - self.context.root.winfo_rootx() + button.winfo_width() / 2
        y = button.winfo_rooty() - self.context.root.winfo_rooty() + button.winfo_height() + self.style.igap
        overlay = CTkFrame(self.context.root)
        overlay.place(x=x, y=y, anchor="n")
        overlay.lift()
        self.filter_overlay = overlay
        self.add_filter_options(overlay)

    def destroy_filter_overlay(self, button: CTkButton):
        try:
            self.filter_overlay.destroy()
        finally:
            return

    def bind_overlay_button(self, button: CTkButton, open_func: callable, close_func: callable):
            def configure_opened():
                button.configure(command=close, text=f"Cancel")
            def configure_closed():
                button.configure(command=open, text=f"Filters")
            def close():
                close_func(button)
                configure_closed()
            def open():
                open_func(button)
                configure_opened()
            def event_callback(event=None):
                close()
            self.context.root.bind("<Escape>", event_callback)
            configure_closed()
    

    def menu_dropdown(self, frame, options: list[str], function):
        med = self.style.get_font()
        dropdown = CTkOptionMenu(
            frame,
            values=options,
            command=function,
            font=med,
            dropdown_font=med
        )
        dropdown.pack(side="left", padx=self.style.gap, pady=self.style.gap, fill="y")
        dropdown.set("None")
        return dropdown
    
    
    

    # ------------------------------------



    def show_stream(self, source: str):
        print(source)

    def root(parent, columns):
        tree = ttk.Treeview(parent, columns=columns, show="headings")
        tree.pack(fill="both", expand=True)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=len(col)*8, anchor="w")

        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def branch():
        return

    def build_frame(self, parent):
        frame = CTkFrame(parent)
        frame.pack(fill="both", expand=True)
        return frame

    def build_tab(self, hack: str):

        if hack in self.tabs:
            return  # already exists

        tab = self.tabview.add(hack)

        textbox = CTkTextbox(
            tab,
            wrap="none",
            state="disabled"
        )
        textbox.pack(fill="both", expand=True)

        self.tabs[hack] = textbox

        # Load previous console history if exists
        for entry in self.context.consoles[hack]:
            if isinstance(entry, str):
                self._append_text(hack, entry)
            else:
                self._append_packet(hack, entry)

    def submit_line(self, hack: str, line: str):

        if hack not in self.tabs:
            self.build_tab(hack)

        self.context.consoles[hack].append(line)
        self._append_text(hack, line)

    def submit_packet(self, hack: str, mpkt: MetaPacket):

        if hack not in self.tabs:
            self.build_tab(hack)

        self.context.consoles[hack].append(mpkt)
        self._append_packet(hack, mpkt)

    def _append_text(self, hack, line):
        textbox = self.tabs[hack]
        textbox.configure(state="normal")
        textbox.insert("end", line + "\n")
        textbox.see("end")
        textbox.configure(state="disabled")

    def _append_packet(self, hack, mpkt: MetaPacket):
        textbox = self.tabs[hack]

        formatted = (
            f"[{mpkt.number}] "
            f"{mpkt.direction.upper()} "
            f"{mpkt.pkt.summary()} "
            f"{mpkt.variable}={mpkt.value}"
        )

        textbox.configure(state="normal")
        textbox.insert("end", formatted + "\n")
        textbox.see("end")
        textbox.configure(state="disabled")