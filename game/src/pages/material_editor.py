from typing import ClassVar

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QScrollArea, QVBoxLayout, QWidget

from ..app_core import Context
from ..widgets.popup import PopupWindow
from .settings import SettingsPage
from .theme_editor import MaterialEditor


class MaterialEditorPopup(MaterialEditor, PopupWindow):
    '''
    Developers: the theme editor's Materials tab in a popup window over
    whatever page is open, so materials can be tuned against the real
    thing. Not modal - the app stays usable behind it. Edits show at once,
    everywhere; Save writes them to the theme's file, like the theme
    editor's. Only one is open at a time (see show_for).
    '''

    # What MaterialEditor's rows need from a SettingsPage (see SettingsSection)
    LABEL_WIDTH = 170
    CONTROL_WIDTH = 300
    SHOW_NOTES = False
    slider = SettingsPage.slider
    section = SettingsPage.section

    open_popup: ClassVar["MaterialEditorPopup | None"] = None

    @classmethod
    def show_for(cls, context: Context):
        '''Opens the popup - or brings the open one to the front.'''
        if cls.open_popup is None:
            cls.open_popup = cls(context)
            cls.open_popup.show()
        cls.open_popup.raise_()
        cls.open_popup.activateWindow()

    def __init__(self, context: Context):
        super().__init__(context.root, context, context.labels.get("material_editor_title"))
        self.labels = context.labels
        self.setModal(False)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        # On closing, not once deleted (later) - so opening it again right away makes a new one
        self.finished.connect(lambda *_: setattr(MaterialEditorPopup, "open_popup", None))

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")
        self.body.addWidget(self.scroll, 1)
        self.build()

        self.save_button = self.add_button(self.labels.get("menu_bar_buttons_theme_editor_save"), self.style.save_theme)
        self.save_button.setToolTip(self.labels.get("menu_bar_tooltips_theme_editor_save"))
        self.add_button(self.labels.get("material_editor_close"), self.close)
        self.style.signals.edited.connect(self.refresh_save)
        self.refresh_save()

        # A theme change (another theme, mode or transparency) needs the rows
        # built again - on a timer, as the control that changed it is still in its signal
        self.rebuild_timer = QTimer(self)
        self.rebuild_timer.setSingleShot(True)
        self.rebuild_timer.setInterval(0)
        self.rebuild_timer.timeout.connect(self.rebuild)
        self.style.signals.changed.connect(self.rebuild_timer.start)

        # Most of the window's height - there are always more rows than fit, and they scroll
        self.resize(self.sizeHint().width(), context.root.height() * 4 // 5)

    def build(self):
        '''The rows, in a fresh body for the scroll area, sized so they never need a horizontal scrollbar.'''
        self.build_materials_tab()
        content = self.scroll.widget().sizeHint().width()
        self.scroll.setMinimumWidth(content + self.style.get_scrollbar_size())

    def rebuild(self):
        scrolled = self.scroll.verticalScrollBar().value()
        self.build()
        self.refresh_save()
        QTimer.singleShot(0, self.scroll, lambda: self.scroll.verticalScrollBar().setValue(scrolled))

    def refresh_save(self):
        style = self.style
        self.save_button.setEnabled(style.is_editable() and style.theme_family() in style.unsaved)

    def new_tab(self, name: str) -> QVBoxLayout:
        '''The scroll area's body, replacing the last one - there's one tab's worth of rows (see SettingsPage.new_tab).'''
        body = QWidget()
        self.style.set_material(body, "none")
        column = QVBoxLayout(body)
        column.setSpacing(self.style.igap)
        column.setContentsMargins(0, 0, self.style.igap, 0)
        column.addStretch(1)
        old = self.scroll.takeWidget()
        if old is not None:
            old.deleteLater()
        self.scroll.setWidget(body)
        return column
