from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget
from .....app_core import Context
from ...base_form import BaseForm


class ModeForm(BaseForm):
    '''
    Read-only "Mode: SUBMARINE/HVAC" label - reads straight from
    context.buffer.defender_status on the animation loop, exactly as it did
    inline in DefenderV0._build_mode_block/_refresh_mode_ui.
    '''

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, process_noun="Mode")

        self.add_header("Operation Mode")

        self.mode_label = QLabel("Mode: —")
        self.mode_label.setFont(self.style.get_font())
        self.mode_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.grid_layout.addWidget(self.mode_label, self.current_row, 0, 1, 3)
        self.current_row += 1

        self.context.animation_manager.add_callback(f"DefenderModeForm_{id(self)}", self.refresh)
        self.refresh()

    def refresh(self):
        submarine_mode = self.context.buffer.defender_status.get("submarine_mode")
        if submarine_mode is None:
            self.mode_label.setText("Mode: —")
            self.mode_label.setStyleSheet("color: gray;")
        elif submarine_mode:
            self.mode_label.setText("Mode: SUBMARINE")
            self.mode_label.setStyleSheet("color: green;")
        else:
            self.mode_label.setText("Mode: HVAC")
            self.mode_label.setStyleSheet("color: orange;")
