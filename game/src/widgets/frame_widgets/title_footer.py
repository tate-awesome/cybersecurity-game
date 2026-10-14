from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget
from ...app_core import Context
from .important_buttons import ImportantButton, OpenProjectRepository, ReportAnIssue


class TitleFooter(QWidget):
    '''
    The line along the bottom of a title page, just above the window's
    Footer: the copyright on the left, links out (to the browser) on the
    right. No background of its own - it sits over the page's visual like
    the title menu does.
    '''

    LINKS: list[type[ImportantButton]] = [OpenProjectRepository, ReportAnIssue]

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master)
        self.context = context
        self.style = context.style
        master.layout().addWidget(self)

        font = QFont("Arial", max(6, round(12 * self.style.ui_scale / 100.0)))
        row = QHBoxLayout(self)
        row.setContentsMargins(self.style.igap, 0, self.style.igap, 0)
        row.setSpacing(self.style.igap)

        copyright_label = QLabel(context.labels.get("title_footer_copyright"))
        copyright_label.setFont(font)
        copyright_label.setTextFormat(Qt.TextFormat.PlainText)
        row.addWidget(copyright_label)
        row.addStretch()

        for link_class in self.LINKS:
            link = link_class(context)
            link.setFont(font)
            link.setCursor(Qt.CursorShape.PointingHandCursor)
            # Not a surface: never tinted (see style.SURFACE_KINDS)
            link.setProperty("surface", "none")
            name = f"_title_link_{id(link)}"
            link.setObjectName(name)
            link.setStyleSheet(self.style.themed(
                f"QPushButton#{name} {{ background: transparent; border: none; padding: 0px;"
                f" color: {self.style.color('text')}; }}"
                f" QPushButton#{name}:hover {{ color: {self.style.color('accent')}; text-decoration: underline; }}"
                f" QPushButton#{name}:pressed {{ color: {self.style.color('text')}; }}"))
            row.addWidget(link)
