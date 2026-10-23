from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QFrame, QPushButton, QScrollArea, QVBoxLayout, QWidget

from ...app_core import Context
from .overlay import Overlay

# Past this many choices, the list scrolls
MAX_SHOWN = 14


class ChoiceList(Overlay):
    '''
    A combo box's list of choices as one of the app's overlays, in place of
    Qt's own popup (see Style's _ComboLists, which opens one for every combo
    box): a button per choice, the current one marked like a selected theme
    (see Style.mark_choice), and its separators. It always drops down below
    the combo box, even from inside another overlay. Picking one sets it
    just as picking from Qt's list would - activated, and the index changed.
    '''

    def __init__(self, context: Context, combo: QComboBox):
        super().__init__(context.root, context, combo, self.fill, trigger_texts=False)
        self.combo = combo

    def placement_anchor(self) -> str:
        return "south"

    def fill(self, overlay: Overlay):
        combo, style = self.combo, self.style
        column = QWidget()
        rows = QVBoxLayout(column)
        rows.setContentsMargins(0, 0, 0, 0)
        rows.setSpacing(2)
        height = 0
        for index in range(combo.count()):
            if combo.itemData(index, Qt.ItemDataRole.AccessibleDescriptionRole) == "separator":
                line = QFrame()
                line.setFixedHeight(1)
                line.setStyleSheet(f"background-color: {style.color('border')}; border: none;")
                rows.addWidget(line)
                continue
            button = QPushButton(combo.itemText(index))
            button.setFont(combo.font())
            # Its own sheet keeps it out of a theme's line colors and lift (see Style.is_plain_button) - it's a list item
            button.setStyleSheet("QPushButton { text-align: left; }")
            tip = combo.itemData(index, Qt.ItemDataRole.ToolTipRole)
            if tip:
                button.setToolTip(tip)
            style.mark_choice(button, index == combo.currentIndex())
            button.clicked.connect(lambda checked=False, index=index: self.pick(index))
            rows.addWidget(button)
            height = max(height, button.sizeHint().height())
        column.setMinimumWidth(combo.width())
        if combo.count() <= MAX_SHOWN:
            self.layout().addWidget(column)
            return
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea, QScrollArea > QWidget > QWidget { background: transparent; }")
        scroll.setWidget(column)
        scroll.setFixedHeight((height + rows.spacing()) * MAX_SHOWN)
        # As wide as the widest choice - the list only scrolls up and down
        scroll.setMinimumWidth(max(column.minimumWidth(), column.sizeHint().width()) + int(style.get_scrollbar_size()))
        self.layout().addWidget(scroll)
        # The current choice in view
        current = rows.itemAt(combo.currentIndex()).widget() if 0 <= combo.currentIndex() < rows.count() else None
        if current is not None:
            scroll.ensureWidgetVisible(current)

    def pick(self, index: int):
        combo = self.combo
        self.hide()
        if index != combo.currentIndex():
            combo.setCurrentIndex(index)
        combo.activated.emit(index)
        combo.textActivated.emit(combo.itemText(index))
