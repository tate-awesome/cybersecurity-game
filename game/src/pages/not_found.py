from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton

from ..app_core import Context
from .page import Page


class NotFound(Page):
    '''
    The 404 page, shown by the Router whenever a requested page doesn't
    exist - including the start page. The usual cause is a missing or
    broken assets folder, so this page deliberately uses nothing from
    assets/ (no labels, no page config): all of its text is hard-coded
    here so it can still explain the problem when assets/ is gone.
    '''

    def __init__(self, context: Context):
        super().__init__(context)
        requested = self.router.missing_page
        if requested == "404":
            # Linked to directly (the demo select page's 404 demo) rather than
            # reached through a missing page - name an obviously fake one
            requested = "nonexistent_page.json"

        title = QLabel("404 - Page Not Found")
        title.setFont(self.style.get_font("title"))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        body = QLabel(
            f"The requested page \"{requested}\" was not found.\n\n"
            "Did you paste the assets folder into the same folder as the executable? "
            "The game looks for it here:\n"
            f"{context.paths.assets}\n\n"
            "Try deleting the current assets folder and downloading it again."
        )
        body.setFont(self.style.get_font("default"))
        body.setAlignment(Qt.AlignmentFlag.AlignCenter)
        body.setWordWrap(True)
        body.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        buttons = QHBoxLayout()
        buttons.addStretch(1)
        # Nothing to go back to when the start page itself is missing
        if len(self.router.navigation_stack) > 1:
            self.add_button(buttons, "Back", self.router.go_back)
        self.add_button(buttons, "Quit", self.router.quit)
        buttons.addStretch(1)

        self.layout().addStretch(1)
        self.layout().addWidget(title)
        self.layout().addWidget(body)
        self.layout().addLayout(buttons)
        self.layout().addStretch(1)

    def add_button(self, layout: QHBoxLayout, text: str, function):
        button = QPushButton(text)
        button.setFont(self.style.get_font("title_btn"))
        button.clicked.connect(lambda checked=False: function())
        layout.addWidget(button)
