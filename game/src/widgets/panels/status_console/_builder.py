from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QPlainTextEdit
from ....app_core import Context
from ...frame_widgets.important_buttons import FreeScrollStatusConsole
from ..panel import Panel

class Builder(Panel):
    KEY = "status_panel"
    # The settings keys (see _packages/_default.json) this panel reads or writes -
    # the workspace editor lists it under each of them
    SETTINGS = (
        "status_console",
    )
    def __init__(self, master, context: Context):
        super().__init__(master, context, self.KEY)

        self.buffer = context.buffer.status

        self.text_box = self.create_text_box(self)

        minimize_button = self.menu_bar.minimize_button(self.text_box, master)

        self.menu_bar.add_important(FreeScrollStatusConsole)

        # Reset print pointer on refresh
        self.buffer.reset_cursor()

        # Start printing loop
        self.context.animation_manager.add_callback(f"status_panel_{id(self)}", self.print_tick)

    def print_tick(self):
        '''
        Prints new status lines to the text box - called every frame.
        The buffer's getter returns all new lines since the last print, so we don't need to loop.
        Empty lines go after every cluster of statuses
        '''
        text_block = self.buffer.get_new_lines()

        # Add to text box - unless the student has switched to free scrolling
        # (status_console "scroll" - see FreeScrollStatusConsole)
        jump_to_bottom = self.context.states.get("status_console", "scroll") != "free"

        if jump_to_bottom and len(text_block) > 0:
            self.text_box.moveCursor(QTextCursor.MoveOperation.End)
            self.text_box.insertPlainText(text_block)
            self.text_box.moveCursor(QTextCursor.MoveOperation.End)
            self.text_box.ensureCursorVisible()

    # Text box
    def create_text_box(self, parent):
        textbox = QPlainTextEdit()
        textbox.setFont(self.style.get_font("mono"))
        textbox.setReadOnly(True)
        textbox.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        # Stretch 1: see Scrollable.__init__ for why (same Panel-body/
        # trailing-filler interaction).
        parent.layout().addWidget(textbox, 1)
        return textbox
