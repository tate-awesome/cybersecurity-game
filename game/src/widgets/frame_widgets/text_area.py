from PySide6.QtWidgets import QTextEdit


class TextArea(QTextEdit):
    '''
    A plain-text box - what QPlainTextEdit would be, except it scrolls by
    the pixel instead of by the line, so the wheel can glide it (see
    SmoothWheel). QPlainTextEdit's scroll bar counts whole lines, so a
    glide could only step a line at a time.

    Plain text in and out, like QPlainTextEdit: the constructor's text and
    anything pasted or dropped in are never read as rich text.
    '''

    def __init__(self, text: str = ""):
        super().__init__()
        self.setAcceptRichText(False)
        self.setPlainText(text)
