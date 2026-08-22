'''
UI blocks shared between DefenderV0 (submarine mode) and HVACView (HVAC mode).
Both build an encryption card, an AP-communication card, and a settings-slider
card with the same structure - they only differ in what data backs the
sliders, what text labels the section, and which method actually sends the
changed values to the AP. Each helper here takes `target` (the DefenderV0 or
HVACView instance) and writes its created widgets onto it via setattr, exactly
matching what the original per-class methods did with `self.`.
'''

from typing import NamedTuple, Callable, Any
from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkSlider
from ...widgets import popup


class SliderDef(NamedTuple):
    title: str
    min_val: float
    max_val: float
    default: float
    attr_name: str
    decimals: int
    data_key: str  # key to read this slider's value from the server-sent data dict


def build_encryption_block(style, parent, popup_master, context, target):
    section = CTkFrame(parent, fg_color=style.color("widget"))
    section.pack(fill="x", padx=style.igap, pady=style.igap)

    CTkLabel(section, text="ENCRYPTION", font=style.get_font()).pack(
        anchor="w", padx=style.igap, pady=(style.igap, 0)
    )
    target._enc_label = CTkLabel(section, text="Status: OFF",
                                  font=style.get_font(), text_color="gray")
    target._enc_label.pack(anchor="w", padx=style.igap)

    # Key entry
    CTkLabel(section, text="Encryption Key", font=style.get_font("small"),
             text_color="gray").pack(anchor="w", padx=style.igap, pady=style.gaptop)
    target._enc_key_entry = CTkEntry(section, font=style.get_font(),
                                      placeholder_text="Enter key…")
    target._enc_key_entry.pack(fill="x", padx=style.igap, pady=(2, 4))

    target._enc_button = CTkButton(section, text="Enable Encryption",
                                    font=style.get_font())

    def enc_button():
        if not target._encryption_on:
            # Encryption is off - try to turn it on
            if target._enc_key_entry.get().strip() == "":
                # Empty key — show error
                popup.message(popup_master, context, "Please enter an encryption key before enabling encryption.")
            elif not str.isascii(target._enc_key_entry.get().strip()):
                # Non-ASCII key — show error
                popup.message(popup_master, context, "Encryption key must be ASCII.")
            else:
                # Key looks good — toggle encryption on behavior
                target._enc_key_entry.configure(state="disabled")
                target._enc_button.configure(text="Disable Encryption")
                target._toggle_encryption()
        else:
            # Encryption is on - turn it off
            target._enc_key_entry.configure(state="normal")
            target._enc_key_entry.delete(0, "end")
            target._enc_button.configure(text="Enable Encryption")
            target._toggle_encryption()

    target._enc_button.configure(command=enc_button)
    target._enc_button.pack(fill="x", padx=style.igap, pady=style.gapbot)


def build_ap_communication_block(style, parent, target, toggle_command: Callable):
    section = CTkFrame(parent, fg_color=style.color("widget"))
    section.pack(fill="x", padx=style.igap, pady=style.igap)

    CTkLabel(section, text="COMMUNICATE VIA ACCESS POINT", font=style.get_font()).pack(
        anchor="w", padx=style.igap, pady=(style.igap, 0)
    )
    target._filter_label = CTkLabel(section, text="Status: OFF",
                                     font=style.get_font(), text_color="gray")
    target._filter_label.pack(anchor="w", padx=style.igap)

    target._filter_button = CTkButton(section, text="Enable Communication Through AP",
                                       font=style.get_font(),
                                       command=toggle_command)
    target._filter_button.pack(fill="x", padx=style.igap, pady=style.gapbot)


def build_slider_block(style, parent, title: str, slider_defs: list[SliderDef],
                        target, on_change: Callable, reset_command: Callable):
    section = CTkFrame(parent, fg_color=style.color("widget"))
    section.pack(fill="x", padx=style.igap, pady=style.igap)

    CTkLabel(
        section,
        text=title,
        font=style.get_font()
    ).pack(anchor="w", padx=style.igap, pady=(style.igap, 8))

    sliders: dict[str, Any] = {}
    slider_value_labels: dict[str, Any] = {}

    for slider_def in slider_defs:
        header = CTkFrame(section, fg_color="transparent")
        header.pack(fill="x", padx=style.igap)

        CTkLabel(
            header,
            text=slider_def.title,
            font=style.get_font("small")
        ).pack(side="left")

        value_label = CTkLabel(
            header,
            text=f"{slider_def.default:.{slider_def.decimals}f}",
            font=style.get_font("small"),
            text_color="gray"
        )
        value_label.pack(side="right")

        def slider_callback(value, lbl=value_label, attr=slider_def.attr_name, d=slider_def.decimals):
            value = float(value)

            setattr(target, attr, value)
            lbl.configure(text=f"{value:.{d}f}")

            # Only send an update when the USER moved the slider.
            if not target._syncing_sliders:
                on_change()

        slider = CTkSlider(
            section,
            from_=slider_def.min_val,
            to=slider_def.max_val,
            command=slider_callback
        )
        slider.set(slider_def.default)
        slider.pack(fill="x", padx=style.igap, pady=(0, 8))

        sliders[slider_def.title] = slider
        slider_value_labels[slider_def.title] = value_label

    reset_button = CTkButton(
        section,
        text="Reset to Defaults",
        font=style.get_font(),
        command=reset_command
    )
    reset_button.pack(
        fill="x",
        padx=style.igap,
        pady=style.igap
    )

    return sliders, slider_value_labels


def sync_sliders(target, data: dict, slider_defs: list[SliderDef], sliders: dict, slider_value_labels: dict):
    '''
    Moves each UI slider to the value the AP most recently reported, and keeps
    target's Python-side attributes synchronized. Caller is responsible for
    any revision-debouncing before calling this (see DefenderV0._sync_submarine_sliders).
    '''
    target._syncing_sliders = True

    try:
        for slider_def in slider_defs:
            value = data.get(slider_def.data_key)
            if value is None:
                continue

            slider = sliders.get(slider_def.title)
            label = slider_value_labels.get(slider_def.title)

            if slider is None:
                continue

            value = float(value)

            # Move the UI slider to the MCU's current value.
            slider.set(value)

            # Keep the Python-side variable synchronized too.
            setattr(target, slider_def.attr_name, value)

            if label is not None:
                label.configure(text=f"{value:.{slider_def.decimals}f}")

    finally:
        target._syncing_sliders = False


def reset_slider_defaults(target, slider_defs: list[SliderDef], sliders: dict,
                           slider_value_labels: dict, post_command: Callable):
    # Prevent each slider.set() from generating its own update
    target._syncing_sliders = True

    try:
        for slider_def in slider_defs:
            # Update Python variable
            setattr(target, slider_def.attr_name, slider_def.default)

            # Move slider
            sliders[slider_def.title].set(slider_def.default)

            # Update displayed number
            slider_value_labels[slider_def.title].configure(
                text=f"{slider_def.default:.{slider_def.decimals}f}"
            )

    finally:
        target._syncing_sliders = False

    post_command()
