from ....app_core import Context
from ... import Overlay

from PySide6.QtWidgets import QCheckBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout
from typing import Callable

class FilterOverlay:
    def __init__(self, button: QPushButton, context: Context, refresh_function: Callable):
        self.context = context
        self.style = context.style
        self.refresh_function = refresh_function

        self.filter_columns = self.context.states.get("packet_filter_categories")
        self.filter_overlay = Overlay(self.context.root, context, button, self.populate_filter_overlay)

    def _checkbox_value(self, slots: dict, key: str):
        '''
        Looks up one checkbox's saved value in the "packet_filter_checkboxes"
        settings category. slots' keys come from a separate settings category
        (self.filter_columns) that isn't guaranteed to stay in sync with it, so
        this raises a clear error instead of a bare KeyError if they drift apart.
        '''
        if key not in slots:
            raise KeyError(f"packet_filter_checkboxes[{key!r}] not found - filter_columns and settings are out of sync")
        return slots[key]


    def populate_filter_overlay(self, overlay: Overlay):
        '''
        Creates a filter overlay just below the button, with checkboxes for each filter in settings["packet_filter_checkboxes"]
        Creates text entries for each filter in self.context.inputs["packet_filter_entries"].
        '''
        apply_filters = lambda: ...

        # Create filter checkbox row - one frame per category, side by side
        box_slots = self.context.states.get("packet_filter_checkboxes")
        checkbox_row = QHBoxLayout()
        checkbox_row.setSpacing(self.style.igap)
        overlay.layout().addLayout(checkbox_row)

        # Create each column of checkboxes based on the hard-coded category
        for category in self.filter_columns:

            category_frame = QFrame()
            category_frame.setStyleSheet(self.style.themed(f"background-color: {self.style.color('widget')};", category_frame))
            category_layout = QVBoxLayout(category_frame)
            category_layout.setContentsMargins(self.style.igap, self.style.igap, self.style.igap, self.style.igap)
            category_layout.setSpacing(self.style.cgap * 2)
            checkbox_row.addWidget(category_frame)

            category_label = QLabel(self.context.labels.get("packet_filter_categories", category))
            category_label.setFont(self.style.get_font())
            category_layout.addWidget(category_label)

            # Create each checkbox in the category
            for filter_key in self.filter_columns[category]:

                filter_box = QCheckBox(self.context.labels.get("packet_filter_checkboxes", filter_key))
                filter_box.setFont(self.style.get_font())
                category_layout.addWidget(filter_box)

                # Load previous input before connecting, so restoring it doesn't itself trigger autosave
                value = self._checkbox_value(box_slots, filter_key)
                filter_box.setChecked(value == "1" or value == 1)

                # Configure for autosave. Stored as "1"/"0" - the convention
                # this settings data already uses everywhere else.
                def autosave(checked: bool, slots=box_slots, key=filter_key):
                    slots[key] = "1" if checked else "0"
                    apply_filters()
                filter_box.toggled.connect(autosave)

        # Create text filter widgets
        text_slots = self.context.states.get("packet_filter_entries")
        entry_frame = QFrame()
        entry_layout = QVBoxLayout(entry_frame)
        entry_layout.setContentsMargins(0, self.style.igap, 0, 0)
        entry_layout.setSpacing(self.style.cgap * 2)
        overlay.layout().addWidget(entry_frame)

        # Create each text filter label and entry
        for text_slot in text_slots:

            filter_label = QLabel(self.context.labels.get("packet_filter_entries", text_slot))
            filter_label.setFont(self.style.get_font())
            entry_layout.addWidget(filter_label)

            filter_entry = QLineEdit()
            filter_entry.setFont(self.style.get_font())
            entry_layout.addWidget(filter_entry)

            # Load previous input
            previous_text = text_slots[text_slot]
            filter_entry.setText(str(previous_text))

            # Configure for autosave
            def autosave(text, slots=text_slots, key=text_slot):
                slots[key] = text
                apply_filters()
            filter_entry.textEdited.connect(autosave)

        # Add filter summary - QLabel word-wraps to its own width automatically,
        # so unlike the tkinter version this doesn't need to track the
        # container's width itself and recompute a wraplength by hand.
        activator_frame = QFrame()
        activator_layout = QHBoxLayout(activator_frame)
        overlay.layout().addWidget(activator_frame)

        summary = self.context.states.get("packet_filter_function", "summary")
        filter_label = QLabel(summary)
        filter_label.setFont(self.style.get_font())
        filter_label.setWordWrap(True)
        activator_layout.addWidget(filter_label)

        def activate():
            self.compile_filter()
            new_summary = self.context.states.get("packet_filter_function", "summary")
            filter_label.setText(new_summary)
            self.refresh_function()

        apply_filters = activate

    def compile_filter(self):
            '''
            Compile and save the mpkt filter to self.function
            The filter ORs within categories (e.g. show packets with any of these protocols),
            and ANDs between categories (e.g. only show packets that match the source filters AND the protocol filters).
            Save the summary to settings["packet_filter_function"]["summary"]
            '''
            # Grab the filter states only when pressing the button
            import copy
            checkbox_slots = copy.deepcopy(self.context.states.get("packet_filter_checkboxes"))
            address_filter = copy.deepcopy(self.context.states.get("packet_filter_entries", "address_filter"))

            def packet_filter(mpkt):

                # Fulfill checkbox conditions
                checkboxes_condition = True
                for category in self.filter_columns:
                    # OR within a category - true if any filter matches, or none are selected
                    category_condition = False
                    none_checked = True
                    for box_name in self.filter_columns[category]:
                        checkbox_value = self._checkbox_value(checkbox_slots, box_name)
                        if checkbox_value == "1" or checkbox_value == 1:
                            none_checked = False
                            category_condition = category_condition or mpkt.matches(category, box_name)
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
                    if (value in mpkt.get("ip_src").lower()
                        or value in mpkt.get("ip_dst").lower()
                        or value in mpkt.get("mac_src").lower()
                        or value in mpkt.get("mac_dst").lower()):
                        address_condition = True
                return address_condition and checkboxes_condition

            # Save the function
            self.function = lambda mpkt: packet_filter(mpkt)

            # Create the summary
            full_summary = "Currently filtering for"

            category_summaries = []
            box_slots = self.context.states.get("packet_filter_checkboxes")
            for category in self.filter_columns:
                category_conditions = []
                category_summary = f"{category}s including"

                for checkbox_key in self.filter_columns[category]:
                    checkbox_value = self._checkbox_value(box_slots, checkbox_key)
                    if checkbox_value == "1" or checkbox_value == 1:
                        category_conditions.append(self.context.labels.get("packet_filter_checkboxes", checkbox_key))

                if len(category_conditions) > 0:
                    category_summary = f"{category_summary} {' OR '.join(category_conditions)}"
                    category_summaries.append(category_summary)
            category_summaries = " AND ".join(category_summaries)

            entry_str = self.context.states.get("packet_filter_entries", "address_filter")
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
            self.context.states.set("packet_filter_function", "summary", value=full_summary)
