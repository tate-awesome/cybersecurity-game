from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QPlainTextEdit
from ....app_core import Context
from ..panel import Panel

class Builder(Panel):
    KEY = "status_panel"
    def __init__(self, master, context: Context):
        super().__init__(master, context, self.KEY)

        self.buffer = context.buffer.status

        self.text_box = self.create_text_box(self)

        # minimize_button = self.menu_bar.minimize_button(self.text_box, master)

        pause_button = self.menu_bar.reversible_button(self.pause, self.unpause, "pause", "unpause")

        jump_button = self.menu_bar.reversible_button(self.unlock_scrolling, self.lock_scrolling, "free_scroll", "live_scroll")

        # Printing Flags
        self.jump_to_bottom = True
        self.run = True

        # Reset print pointer on refresh
        self.buffer.reset_cursor()

        # Start printing loop
        self.start_printing()


    def start_printing(self):
        self.run = True
        self.context.animation_manager.add_callback("status_panel", self.print_tick)

    def stop_printing(self):
        self.run = False
        self.context.animation_manager.remove_callback("status_panel")

    def print_tick(self):
        '''
        Prints new status lines to the text box, then sets a timer to call itself again after 100 ms.
        The buffer's getter returns all new lines since the last print, so we don't need to loop.
        Empty lines go after every cluster of statuses
        '''
        text_block = self.buffer.get_new_lines()

        # Add to text box

        if self.jump_to_bottom and len(text_block) > 0:
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
        parent.layout().addWidget(textbox)
        return textbox

    # Buttons
    def pause(self):
        self.stop_printing()

    def unpause(self):
        self.start_printing()

    def unlock_scrolling(self):
        self.jump_to_bottom = False

    def lock_scrolling(self):
        self.jump_to_bottom = True
