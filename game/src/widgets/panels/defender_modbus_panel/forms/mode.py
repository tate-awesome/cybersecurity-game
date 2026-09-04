from customtkinter import CTkFrame, CTkLabel
from .....app_core import Context
from ...base_form import BaseForm


class ModeForm(BaseForm):
    '''
    Read-only "Mode: SUBMARINE/HVAC" label - reads straight from
    context.buffer.defender_status on the animation loop, exactly as it did
    inline in DefenderV0._build_mode_block/_refresh_mode_ui.
    '''

    def __init__(self, master: CTkFrame, context: Context):
        super().__init__(master, context, attack_noun="Mode")

        self.add_header("Operation Mode")

        self.mode_label = CTkLabel(self, text="Mode: —", font=self.style.get_font(), anchor="w")
        self.mode_label.grid(row=self.current_row, column=0, columnspan=3, sticky="ew",
                              pady=self.style.gapbot, padx=self.style.gap)
        self.current_row += 1

        self.context.animation_manager.add_callback(f"DefenderModeForm_{id(self)}", self.refresh)
        self.refresh()

    def refresh(self):
        submarine_mode = self.context.buffer.defender_status.get("submarine_mode")
        if submarine_mode is None:
            self.mode_label.configure(text="Mode: —", text_color="gray")
        elif submarine_mode:
            self.mode_label.configure(text="Mode: SUBMARINE", text_color="green")
        else:
            self.mode_label.configure(text="Mode: HVAC", text_color="orange")
