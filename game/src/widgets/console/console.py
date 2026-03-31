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

        parent.configure(fg_color=style.color("root"))

        # Filter overlay
        menu_frame = self.create_menu_frame(self.frame)
        refresh_button = self.create_menu_button(menu_frame, "Refresh")
        filter_button = self.create_menu_button(menu_frame, "Filters")
        self.bind_overlay_button(filter_button, self.create_filter_overlay, self.destroy_filter_overlay)

        # Designate menu filters


        # Create treeview
    
    # Menu
    def create_menu_frame(self, parent):
        menu_frame = CTkFrame(parent)
        menu_frame.pack(side="top", fill="x")
        return menu_frame
    
    def create_menu_button(self, frame, text, function=None):
        med = self.style.get_font()
        button = CTkButton(frame, text=text, command=function, font=med)
        button.pack(side="left", padx=self.style.gap, pady=self.style.gap)
        return button
    
    # Filter overlay
    def add_filter_activator(self, parent: CTkFrame):
        med = self.style.get_font()

        activator_frame = CTkFrame(parent)
        activator_frame.pack(side="top", padx=self.style.gap2, pady=self.style.gap2, fill="x")

        activator_button = CTkButton(activator_frame, text="Apply Filters", font=med)
        activator_button.pack(side="left", anchor="w", padx=self.style.gap, pady=self.style.gap)

        summary = self.context.inputs["packet_filter_function"]["summary"]
        activator_frame.update_idletasks()
        width = activator_frame.winfo_width() - activator_button.winfo_width() - 50

        filter_label = CTkLabel(activator_frame, text=summary, font=med, wraplength=width, justify="left")
        filter_label.pack(side="left", anchor="w", padx=self.style.gap, pady=self.style.gap, fill="x")

        def activate():
            self.compile_filter()
            new_summary = self.context.inputs["packet_filter_function"]["summary"]

            width = activator_frame.winfo_width() - activator_button.winfo_width() - 50

            filter_label.configure(text=new_summary, wraplength=width)

            self.buffer.console_buffers["sniff"]

            self.buffer.print_filtered_console_buffer("sniff", self.context.inputs["packet_filter_function"]["function"])

        activator_button.configure(command=activate)

    def add_filter_options(self, parent: CTkFrame):
        '''
        Create filter menu widgets, load filter options from context and configure inputs for autosave
        '''
        # Create box filter widgets
        box_slots = self.context.inputs["checkbox_filters"]
        med = self.style.get_font()
        checkbox_frame = CTkFrame(parent, fg_color=self.style.color("panel"))
        checkbox_frame.pack(side="top", padx=self.style.gap, pady=self.style.gaptop)

        for category in box_slots:

            category_frame = CTkFrame(checkbox_frame, fg_color=self.style.color("widget"))
            category_frame.pack(side="left", padx=self.style.gap, pady=self.style.gap, anchor="n")
            category_label = CTkLabel(category_frame, text=category, font=med)
            category_label.pack(side="top", pady=self.style.gap, anchor="n")

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
        entry_frame.pack(side="top", fill="x", padx=self.style.gap2, pady=self.style.gap2)

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
        overlay = CTkFrame(self.context.root, border_color=self.style.color("accent"), border_width=2)
        overlay.place(x=x, y=y, anchor="n")
        overlay.lift()
        self.filter_overlay = overlay
        self.add_filter_options(overlay)
        self.add_filter_activator(overlay)

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

    def compile_filter(self):
            '''
            Compile and save the mpkt filter to self.context.inputs["packet_filter_function"]["function"]
            Save the summary to self.context.inputs["packet_filter_function"]["summary"]
            '''
            # Compile section
            def checkbox_filter(mpkt):
                checkboxes_condition = True
                box_slots = self.context.inputs["checkbox_filters"]
                for category in box_slots:
                    # OR within a category - show only all checked :: start false, become true if any match
                    any_checked = False
                    category_condition = False
                    for box_name in box_slots[category]:
                        if box_slots[category][box_name]["state"] == "1":
                            any_checked = True
                            category_condition = category_condition or box_slots[category][box_name]["function"](mpkt)

                    if not any_checked: category_condition = True # If none checked, show all

                    # AND each category condition together :: if any miss, return false
                    checkboxes_condition = checkboxes_condition and category_condition
                return checkboxes_condition

            def address_filter(mpkt):
                filter_str = self.context.inputs["text_filters"]["address_filter"]["text"]
                addresses = filter_str.split("|")
                if len(addresses) < 1:
                    return True
                condition_met = False
                # If any given address matches any mpkt address, return true
                for address in addresses:
                    value = str.strip(address.lower())
                    if (value in mpkt.ip_src.lower()
                        or value in mpkt.ip_dst.lower()
                        or value in mpkt.mac_src.lower()
                        or value in mpkt.mac_dst.lower()):
                        condition_met = True
                return condition_met
            
            # Save function
            self.context.inputs["packet_filter_function"]["function"] = lambda mpkt: address_filter(mpkt) and checkbox_filter(mpkt)

            # Summarize section
            full_summary = "Currently filtering for"
            category_summaries = []
            box_slots = self.context.inputs["checkbox_filters"]
            for category in box_slots:
                category_conditions = []
                category_summary = f"{category}s including"

                for box_name in box_slots[category]:
                    if box_slots[category][box_name]["state"] == "1":
                        category_conditions.append(box_name)

                if len(category_conditions) > 0:
                    category_summary = f"{category_summary} {" OR ".join(category_conditions)}"
                    category_summaries.append(category_summary)
            category_summaries = " AND ".join(category_summaries)

            filter_str = self.context.inputs["text_filters"]["address_filter"]["text"]
            addresses = filter_str.split("|")
            
            if len(addresses) < 1 or len(filter_str) < 1:
                if len(category_summaries) < 1:
                    full_summary = f"{full_summary} any packets."
                else:
                    full_summary = f"{full_summary} packets with {category_summaries}."
            else:
                for a in addresses:
                    a = f"\"{a}\""
                addresses = " OR ".join(addresses).lower()
                if len(category_summaries) < 1:
                    full_summary = f"{full_summary} packets involving addresses matching {addresses}."
                else:
                    full_summary = f"{full_summary} packets with {category_summaries}, and involving addresses matching {addresses}."

            # Save summary
            self.context.inputs["packet_filter_function"]["summary"] = full_summary
    

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