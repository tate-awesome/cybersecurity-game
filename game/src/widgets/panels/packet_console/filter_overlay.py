from ....app_core.context import Context
from ....network.meta_packet import MetaPacket
from ....network.data_buffer import DataBuffer
from ... import Overlay

from typing import cast
import customtkinter as ctk
from customtkinter import *
from tkinter import ttk
import tkinter as tk

class FilterOverlay:
    def __init__(self, button, context: Context, refresh_function):
        self.context = context
        self.style = context.style
        self.buffer = cast(DataBuffer, context.net.data_buffer)
        self.refresh_function = refresh_function

        self.filter_columns = {
            "source": [
                "nmap",
                "arp",
                "dos",
                "sniff",
                "mitm",
                "pcap"
            ],
            "protocol": [
                "TCP",
                "ARP",
                "UDP",
                "DNS",
                "MODBUSADU",
                "WRITE SINGLE REGISTER",
                "READ HOLDING REGISTERS RESPONSE"
            ],
            "direction": [
                "out",
                "in",
                "other"
            ]
        }
        self.filter_overlay = Overlay(self.context.root, context, button, self.populate_filter_overlay)


    def populate_filter_overlay(self, overlay):
        '''
        Creates a filter overlay just below the button, with checkboxes for each filter in self.context.states["packet_filter_checkboxes"]
        Creates text entries for each filter in self.context.inputs["packet_filter_entries"].
        '''
        apply_filters = lambda: ...

        # Save reference for later destruction

        # Create filter checkbox frame
        box_slots = self.context.states["packet_filter_checkboxes"]
        checkbox_frame = CTkFrame(overlay, fg_color=self.style.color("panel"))
        checkbox_frame.pack(side="top", padx=self.style.gap, pady=self.style.gaptop)

        # Create each column of checkboxes based on the hard-coded category
        for category in self.filter_columns:

            category_frame = CTkFrame(checkbox_frame, fg_color=self.style.color("widget"))
            category_frame.pack(side="left", padx=self.style.gap, pady=self.style.gap, anchor="n")
            category_label = CTkLabel(category_frame, text=self.context.labels["packet_filter_categories"][category], font=self.style.get_font())
            category_label.pack(side="top", pady=self.style.gap, anchor="n")

            # Create each checkbox in the category
            for filter_key in self.filter_columns[category]:

                filter_box = CTkCheckBox(category_frame, text=self.context.labels["packet_filter_checkboxes"][filter_key], font=self.style.get_font())
                filter_box.pack(side="top", anchor="w", pady=self.style.gap, padx=self.style.gap)
                
                # Load previous input
                value = box_slots[filter_key]
                if value == "1" or value == 1: filter_box.select()
                else: filter_box.deselect()
                
                # Configure for autosave
                def autosave(slots=box_slots, key=filter_key, b=filter_box):
                    slots[key] = str(b.get())
                    apply_filters()
                filter_box.configure(command=autosave)
        
        # Create text filter widgets
        text_slots = self.context.states["packet_filter_entries"]
        entry_frame = CTkFrame(overlay)
        entry_frame.pack(side="top", fill="x", padx=self.style.gap2, pady=self.style.gap2)

        # Create each text filter label and entry
        for text_slot in text_slots:

            filter_label = CTkLabel(entry_frame, text=self.context.labels["packet_filter_entries"][text_slot], font=self.style.get_font())
            filter_label.pack(side="top", padx=self.style.gap, pady=self.style.gaptop)
            filter_entry = CTkEntry(entry_frame, font=self.style.get_font())
            filter_entry.pack(fill="x", side="top", padx=self.style.gap, pady=self.style.gap)
            
            # Load previous input
            previous_text = text_slots[text_slot]
            filter_entry.delete(0, "end")
            filter_entry.insert(0, previous_text)

            # Configure for autosave
            def autosave(event=None, slots=text_slots, key=text_slot, e=filter_entry):
                slots[key] = str(e.get())
                apply_filters()
            filter_entry.bind("<KeyRelease>", autosave)

        # Add filter activator button and summary
        activator_frame = CTkFrame(overlay)
        activator_frame.pack(side="top", padx=self.style.gap2, pady=self.style.gap2, fill="x")

        # activator_button = CTkButton(activator_frame, text="Apply Filters", font=self.style.get_font())
        # activator_button.pack(side="left", anchor="w", padx=self.style.gap, pady=self.style.gap)

        summary = self.context.states["packet_filter_function"]["summary"]
        width = activator_frame.winfo_width() - 50

        filter_label = CTkLabel(activator_frame, text=summary, font=self.style.get_font(), justify="left", wraplength=width/self.style.get_scale_correction())
        filter_label.pack(side="left", anchor="w", padx=self.style.gap, pady=self.style.gap, fill="x")

        def activate():
            self.compile_filter()
            new_summary = self.context.states["packet_filter_function"]["summary"]

            width = activator_frame.winfo_width() - 50

            filter_label.configure(text=new_summary, wraplength=width/self.style.get_scale_correction())

            self.refresh_function()
        
        apply_filters = activate

        # activator_button.configure(command=activate)

    def compile_filter(self):
            '''
            Compile and save the mpkt filter to self.context.states["packet_filter_function"]["function"]
            The filter ORs within categories (e.g. show packets with any of these protocols),
            and ANDs between categories (e.g. only show packets that match the source filters AND the protocol filters).
            Save the summary to self.context.states["packet_filter_function"]["summary"]
            '''
            # Grab the filter states only when pressing the button
            import copy
            checkbox_slots = copy.deepcopy(self.context.states["packet_filter_checkboxes"]) 
            address_filter = copy.deepcopy(self.context.states["packet_filter_entries"]["address_filter"])
            
            def packet_filter(mpkt):

                # Fulfill checkbox conditions
                checkboxes_condition = True
                for category in self.filter_columns:
                    # OR within a category - true if any filter matches, or none are selected
                    category_condition = False
                    none_checked = True
                    for box_name in self.filter_columns[category]:
                        if checkbox_slots[box_name] == "1" or checkbox_slots[box_name] == 1:
                            none_checked = False
                            category_condition = category_condition or mpkt.matches(box_name)
                    category_condition = category_condition or none_checked

                    # AND each category condition together :: if any miss, return false
                    checkboxes_condition = checkboxes_condition and category_condition
                # checkboxes_condition is now set

                # Fulfill text entry conditions (custom)
                addresses = address_filter.split("|")
                address_condition = False
                if len(addresses) < 1:
                    address_condition = True
                # If any given address matches any mpkt address, return true
                for address in addresses:
                    value = str.strip(address.lower())
                    if (value in mpkt.ip_src.lower()
                        or value in mpkt.ip_dst.lower()
                        or value in mpkt.mac_src.lower()
                        or value in mpkt.mac_dst.lower()):
                        address_condition = True
                return address_condition and checkboxes_condition
            
            # Save the function
            self.context.states["packet_filter_function"]["function"] = lambda mpkt: packet_filter(mpkt)

            # Create the summary
            full_summary = "Currently filtering for"

            category_summaries = []
            box_slots = self.context.states["packet_filter_checkboxes"]
            for category in self.filter_columns:
                category_conditions = []
                category_summary = f"{category}s including"

                for checkbox_key in self.filter_columns[category]:
                    if box_slots[checkbox_key] == "1" or box_slots[checkbox_key] == 1:
                        category_conditions.append(self.context.labels["packet_filter_checkboxes"][checkbox_key])

                if len(category_conditions) > 0:
                    category_summary = f"{category_summary} {' OR '.join(category_conditions)}"
                    category_summaries.append(category_summary)
            category_summaries = " AND ".join(category_summaries)

            entry_str = self.context.states["packet_filter_entries"]["address_filter"]
            print(entry_str)
            addresses = entry_str.split("|")
            
            if len(addresses) < 1 or len(entry_str) < 1:
                if len(category_summaries) < 1:
                    full_summary = f"{full_summary} any packets."
                else:
                    full_summary = f"{full_summary} packets with {category_summaries}."
            else:
                for a in addresses:
                    a = f"\"{a}\""
                addresses = " OR ".join(addresses).lower()
                if len(category_summaries) < 1:
                    full_summary = f"{full_summary} packets involving addresses matching \"{addresses}\"."
                else:
                    full_summary = f"{full_summary} packets with {category_summaries}, and involving addresses matching {addresses}."

            # Save summary
            self.context.states["packet_filter_function"]["summary"] = full_summary