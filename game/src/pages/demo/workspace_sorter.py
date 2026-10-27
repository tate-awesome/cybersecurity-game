import copy
import json
import re

from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import QCheckBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from ...app_core import Context
from ...widgets import MenuBar, Scrollable, modal
from ...widgets.frame_widgets.drag_drop import DragHandle, DragPayload, DropZone, ListZone
from ...widgets.frame_widgets.important_buttons import PAGE_MARK, POPUP_MARK, WARNING_MARK
from ..page import Page
from .config_editor import (DeleteWorkspaceDialog, NewWorkspaceDialog, RenameWorkspaceDialog, delete_workspace, make_workspace,
                            rename_workspace, write_config_values)

WORKSPACE = "workspace"
SECTION = "section"


def checkbox(context: Context, label: str, checked: bool, tooltip: str, toggled) -> QCheckBox:
    box = QCheckBox(context.labels.get(label))
    box.setFont(context.style.get_font("default"))
    box.setChecked(checked)
    box.setToolTip(context.labels.get(tooltip))
    box.toggled.connect(toggled)
    return box


class WorkspaceChip(QFrame):
    '''
    One workspace on the sorter, a full-width row: its name, dragged to
    reorder or recategorize it, a checkbox for whether the workspace
    select page lists it ("include") - a hidden one stays where it is,
    faded - buttons to rename or delete it, and links to edit it in the
    workspace editor and to open it. rename, delete, edit and open_ are
    called with its key.
    '''

    def __init__(self, context: Context, key: str, name: str, shown: bool, changed, edit, open_, rename, delete):
        super().__init__()
        self.key = key
        self.name = name
        self.zone: DropZone | None = None
        self.style = context.style
        context.style.set_material(self, "card", rounded=True, outlined=True)
        layout = QHBoxLayout(self)
        gap = context.style.cgap * 2
        layout.setContentsMargins(gap * 2, gap, gap * 2, gap)
        layout.setSpacing(gap * 2)
        self.label = QLabel(name)
        self.label.setFont(context.style.get_font("default"))
        layout.addWidget(self.label, 1)
        self.shown = checkbox(context, "workspace_sorter_shown", shown, "workspace_sorter_shown_tooltip",
                              lambda checked: (self.show_state(), changed()))
        layout.addWidget(self.shown)
        for label, mark, action in (("rename", POPUP_MARK, rename), ("delete", WARNING_MARK, delete)):
            button = QPushButton(f"{context.labels.get(f'workspace_sorter_{label}_workspace')} {mark}")
            button.setFont(context.style.get_font("default"))
            button.setToolTip(context.labels.get(f"workspace_sorter_{label}_workspace_tooltip"))
            button.clicked.connect(lambda checked=False, action=action: action(self.key))
            layout.addWidget(button)
        for label, action in (("edit", edit), ("open", open_)):
            button = QPushButton(f"{context.labels.get(f'workspace_sorter_{label}_workspace')} {PAGE_MARK}")
            button.setFont(context.style.get_font("default"))
            button.setToolTip(context.labels.get(f"workspace_sorter_{label}_workspace_tooltip"))
            button.clicked.connect(lambda checked=False, action=action: action(self.key))
            layout.addWidget(button)
        self.show_state()
        DragHandle(self, lambda: DragPayload(WORKSPACE, self.key, self.zone.zone_id))

    def set_name(self, name: str):
        self.name = name
        self.label.setText(name)

    def number(self, position: int | None):
        '''Shows its place in a numbered section - as the select page numbers it - or just its name.'''
        self.label.setText(self.name if position is None else f"{position}. {self.name}")

    def show_state(self):
        self.style.set_tone(self.label, None if self.shown.isChecked() else "muted")


class CategoryChip(QFrame):
    '''
    A category's stand-in in the sidebar, by its title: dragged to reorder
    the categories without scrolling past their cards, and clicked to
    scroll to its card.
    '''

    def __init__(self, context: Context, title: str, clicked):
        super().__init__()
        self.clicked = clicked
        context.style.set_material(self, "card", rounded=True, outlined=True)
        layout = QHBoxLayout(self)
        gap = context.style.cgap * 2
        layout.setContentsMargins(gap * 2, gap, gap * 2, gap)
        self.label = QLabel(title)
        self.label.setFont(context.style.get_font("default"))
        self.label.setWordWrap(True)
        layout.addWidget(self.label)
        self.setToolTip(context.labels.get("workspace_sorter_category_chip_tooltip"))

    def mouseReleaseEvent(self, event):
        # A drag's release never gets here - its DragHandle takes it
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(event.position().toPoint()):
            self.clicked()
        super().mouseReleaseEvent(event)


class SectionCard(QFrame):
    '''
    A category of workspaces - one select page section - as a card: its
    title (dragged to reorder the categories) with its own controls beside
    it, above a ListZone of its workspaces, and a button to make a new
    workspace in it. section is None for the Not Listed card, which has no
    controls and takes no drops.
    '''

    def __init__(self, page: "WorkspaceSorter", zone_id: str, title: str, section: dict | None, note: str = ""):
        super().__init__()
        context = page.context
        self.zone_id = zone_id
        self.section = section
        self.style = context.style
        # Its sidebar chip (see WorkspaceSorter.add_section) - None for Not Listed
        self.chip: CategoryChip | None = None
        self.changed = page.mark_dirty
        context.style.set_material(self, "panel", rounded=True, outlined=True)
        layout = QVBoxLayout(self)
        pad = context.style.igap
        layout.setContentsMargins(pad, pad, pad, pad)
        layout.setSpacing(context.style.cgap * 2)

        self.header = QWidget()
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(pad)
        self.heading = QLabel(title)
        self.heading.setFont(context.style.get_font("title_btn"))
        header_layout.addWidget(self.heading, 1)
        if note:
            hint = QLabel(note)
            hint.setFont(context.style.get_font("default"))
            context.style.set_tone(hint, "muted")
            header_layout.addWidget(hint)
        if section is not None:
            header_layout.addWidget(checkbox(context, "workspace_sorter_numbered", bool(section.get("numbered")),
                                             "workspace_sorter_numbered_tooltip", self.set_numbered))
            header_layout.addWidget(checkbox(context, "workspace_sorter_shown", not section.get("hidden"),
                                             "workspace_sorter_category_shown_tooltip", self.set_shown))
            remove = QPushButton(context.labels.get("workspace_sorter_remove_category"))
            remove.setFont(context.style.get_font("default"))
            remove.setToolTip(context.labels.get("workspace_sorter_remove_category_tooltip"))
            remove.clicked.connect(lambda checked=False: page.remove_section(self))
            header_layout.addWidget(remove)
        layout.addWidget(self.header)

        self.chips = ListZone(context, zone_id, {WORKSPACE} if section is not None else set(),
                              spacing=context.style.cgap * 2)
        layout.addWidget(self.chips)

        new = QPushButton(f"{context.labels.get('workspace_sorter_new_workspace')} {POPUP_MARK}")
        new.setFont(context.style.get_font("default"))
        new.setToolTip(context.labels.get("workspace_sorter_new_workspace_tooltip"))
        new.clicked.connect(lambda checked=False: page.new_workspace(self))
        new_row = QHBoxLayout()
        new_row.addStretch(1)
        new_row.addWidget(new)
        layout.addLayout(new_row)
        self.show_state()

    def set_numbered(self, numbered: bool):
        if numbered:
            self.section["numbered"] = True
        else:
            self.section.pop("numbered", None)
        self.changed()

    def set_shown(self, shown: bool):
        if shown:
            self.section.pop("hidden", None)
        else:
            self.section["hidden"] = True
        self.show_state()
        self.changed()

    def show_state(self):
        hidden = self.section is not None and self.section.get("hidden")
        self.style.set_tone(self.heading, "muted" if hidden else None)
        if self.chip is not None:
            self.style.set_tone(self.chip.label, "muted" if hidden else None)


class WorkspaceSorter(Page):
    '''
    Developer page for sorting and categorizing workspaces - what the
    workspace select page lists, under which section, in which order -
    by dragging instead of editing each workspace's config. One column:

      - Each category - a select page section (title/select_workspace's
        "sections") - is a card listing its workspaces top to bottom. Drag
        a workspace within a card to reorder it, or onto another card to
        move it to that category ("category").
      - A workspace can also sit on its own between, above or below the
        categories - listed outside any, like Start Here! ({"workspace":
        its key} in "sections", and no "category"). Drag it there, or
        back into a category.
      - Drag a card by its title - or its chip in the Categories sidebar
        on the left, which never scrolls away - to reorder the categories.
        Clicking a chip scrolls to its card. A card's Numbered
        checkbox numbers its workspaces on the select page, Shown lists
        the whole category there or not ("hidden"), and Remove takes it
        away - its workspaces go to Not Listed.
      - Each workspace's Shown checkbox is its "include" - a hidden one
        keeps its place, for whenever it's shown again - Rename gives it a
        new name and folder, Delete deletes it for good, its Edit button
        opens it in the workspace editor, and Open opens the workspace
        itself.
      - Add Category, under the cards, adds an empty one with the name
        typed beside it.
      - Workspaces neither in a category nor on their own sit in Not
        Listed at the bottom - drag one into a category, or between them,
        to list it.
      - New Workspace, under each card, makes a workspace in it right
        away (see make_workspace) - in Not Listed, with no category.

    Nothing is written until Save, which sets every workspace's
    "category", "order" and "include" in its config.json - only the files
    that change - and the categories and workspaces on their own in
    title/select_workspace's config.json, adding a new category's name to
    the labels. Discard
    Changes rebuilds the page from the files.
    '''

    SELECT_PAGE = "title/select_workspace"
    NOT_LISTED = "_not_listed"
    COLUMN_WIDTH = 820
    SIDEBAR_WIDTH = 240

    def __init__(self, context: Context):
        super().__init__(context)
        self.labels = context.labels
        self.pages = context.pages
        self.dirty = False
        # Labels new categories need, written on Save: key -> name
        self.new_labels: dict[str, str] = {}

        menu_bar = MenuBar(self, context, "workspace_sorter")
        from ...widgets.frame_widgets.important_buttons import OpenWorkspaceSelect, developer_text
        menu_bar.game_label.setText(developer_text(menu_bar.game_label.text()))
        menu_bar.add_button("save_workspace_order", self.save)
        menu_bar.add_button("discard_workspace_order", lambda: self.router.refresh(save=False))
        menu_bar.add_important(OpenWorkspaceSelect)

        select_config = self.raw_config(self.SELECT_PAGE)
        self.sections: list[dict] = [section for section in select_config.get("sections", [])
                                     if isinstance(section, dict)]
        link_folder = select_config.get("link_folder", "workspaces")
        self.workspaces = {key: self.raw_config(key) for key in self.pages.pages_in(link_folder)}

        # The categories sidebar on the left, beside the scrolling cards
        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(self.style.igap)
        self.layout().addWidget(body, 1)
        sidebar = Scrollable(body, context)
        sidebar.setFixedWidth(self.SIDEBAR_WIDTH)
        sidebar.columnconfigure(0, 1)
        sidebar_heading = QLabel(self.labels.get("workspace_sorter_categories"))
        sidebar_heading.setFont(self.style.get_font("title_btn"))
        sidebar.grid_layout.addWidget(sidebar_heading, 0, 0)
        self.category_list = ListZone(context, "categories", {SECTION}, spacing=self.style.cgap * 2)
        self.category_list.dropped.connect(lambda payload, slot: self.drop_section(payload, slot, self.category_list))
        sidebar.grid_layout.addWidget(self.category_list, 1, 0)
        sidebar.add_deadspace()

        scrollable = Scrollable(body, context)
        self.scrollable = scrollable
        scrollable.columnconfigure(0, 1)
        self.style.set_material(scrollable, "none")
        scrollable.viewport().setAutoFillBackground(False)
        self.style.set_material(scrollable.inner, "none")

        # One column down the middle, no wider than COLUMN_WIDTH
        row = QHBoxLayout()
        row.addStretch(1)
        column = QWidget()
        column.setMaximumWidth(self.COLUMN_WIDTH)
        row.addWidget(column, 100)
        row.addStretch(1)
        scrollable.grid_layout.addLayout(row, 0, 0)
        column_layout = QVBoxLayout(column)
        column_layout.setContentsMargins(0, 0, 0, 0)
        column_layout.setSpacing(self.style.igap)

        intro = QLabel(self.labels.get("workspace_sorter_intro"))
        intro.setFont(self.style.get_font("default"))
        intro.setWordWrap(True)
        column_layout.addWidget(intro)

        # The categories' cards, and the workspaces on their own between them (see drop_listed)
        self.section_list = ListZone(context, "sections", {SECTION, WORKSPACE})
        self.section_list.dropped.connect(self.drop_listed)
        column_layout.addWidget(self.section_list)

        self.cards: dict[str, SectionCard] = {}
        self.chips: dict[str, WorkspaceChip] = {}
        for section in self.sections:
            if "workspace" in section:
                if section["workspace"] in self.workspaces and section["workspace"] not in self.chips:
                    self.add_chip(section["workspace"], self.section_list)
            else:
                self.add_section(copy.deepcopy(section), self.labels.get(f'title_buttons_{section.get("label", "_default")}'))

        column_layout.addWidget(self.build_new_category_row())

        # Only ever dragged out of - a workspace is listed by being in a category
        self.not_listed = SectionCard(self, self.NOT_LISTED, self.labels.get("workspace_sorter_not_listed"), None,
                                      self.labels.get("workspace_sorter_not_listed_note"))
        self.cards[self.NOT_LISTED] = self.not_listed
        column_layout.addWidget(self.not_listed)

        ordered = sorted(self.workspaces.items(), key=lambda item: (self.number_or_zero(item[1].get("order")), item[0]))
        for key, config in ordered:
            if key not in self.chips:
                self.add_chip(key, self.cards.get(self.zone_id(config.get("category")), self.not_listed).chips)
        scrollable.add_deadspace()

        self.status = QLabel()
        self.status.setFont(self.style.get_font("default"))
        self.status.setWordWrap(True)
        self.layout().addWidget(self.status)

        self.renumber()

    @staticmethod
    def zone_id(category) -> str:
        return f"section:{category}"

    @staticmethod
    def number_or_zero(value) -> float:
        return value if isinstance(value, (int, float)) and not isinstance(value, bool) else 0

    def raw_config(self, key: str) -> dict:
        '''A page's config.json as written - not _ref-resolved (see PageManager.load_page_config), to compare saves against.'''
        path = self.pages.config_paths.get(key)
        if path is None:
            return {}
        return json.loads(path.read_text(encoding="utf-8"))

    def add_chip(self, key: str, zone: DropZone):
        '''A chip for workspace key, at the bottom of zone - a card's, or the list of categories, on its own.'''
        chip = WorkspaceChip(self.context, key, self.labels.get(self.pages.link_label(key)),
                             self.workspaces[key].get("include") == 1, self.mark_dirty, self.edit_workspace,
                             self.open_workspace, self.rename_workspace, self.delete_workspace)
        self.chips[key] = chip
        chip.zone = zone
        zone.insert(chip, len(zone.items))

    # Categories
    def add_section(self, section: dict, title: str) -> SectionCard:
        '''A card for section, at the bottom of the list, draggable by its header - and its chip, at the bottom of the sidebar.'''
        card = SectionCard(self, self.zone_id(section.get("category")), title, section)
        card.chips.dropped.connect(lambda payload, slot, zone=card.chips: self.drop_workspace(payload, zone, slot))
        self.cards[card.zone_id] = card
        self.section_list.insert(card, len(self.section_list.items))
        DragHandle(card.header, lambda: DragPayload(SECTION, card.zone_id, self.section_list.zone_id), preview=card)
        card.chip = CategoryChip(self.context, title, lambda: self.scroll_to(card))
        card.show_state()
        self.category_list.insert(card.chip, len(self.category_list.items))
        DragHandle(card.chip, lambda: DragPayload(SECTION, card.zone_id, self.category_list.zone_id))
        return card

    def scroll_to(self, card: SectionCard):
        '''Scrolls the cards so card's top is at the top.'''
        top = card.mapTo(self.scrollable.inner, QPoint(0, 0)).y()
        self.scrollable.verticalScrollBar().setValue(top - self.style.igap)

    def build_new_category_row(self) -> QWidget:
        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(self.style.igap)
        self.new_name = QLineEdit()
        self.new_name.setFont(self.style.get_font("default"))
        self.new_name.setPlaceholderText(self.labels.get("workspace_sorter_new_category_placeholder"))
        self.new_name.returnPressed.connect(self.new_section)
        layout.addWidget(self.new_name, 1)
        button = QPushButton(self.labels.get("workspace_sorter_add_category"))
        button.setFont(self.style.get_font("default"))
        button.clicked.connect(lambda checked=False: self.new_section())
        layout.addWidget(button)
        return row

    def new_section(self):
        '''Adds an empty category named whatever's typed - its id and label made from the name.'''
        name = self.new_name.text().strip()
        if not name:
            self.set_status(self.labels.get("workspace_sorter_name_needed"), "bad")
            return
        base = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") or "category"
        # Not one a workspace already names, either - it would land in the new category by surprise
        taken = {card.section.get("category") for card in self.cards.values() if card.section is not None}
        taken |= {config.get("category") for config in self.workspaces.values()}
        slug, number = base, 1
        while slug in taken or f"title_buttons_{slug}" in self.labels.data or f"title_buttons_{slug}" in self.new_labels:
            number += 1
            slug = f"{base}_{number}"
        self.new_labels[f"title_buttons_{slug}"] = name
        self.add_section({"label": slug, "category": slug}, name)
        self.new_name.clear()
        self.mark_dirty()

    def remove_section(self, card: SectionCard):
        '''Takes a category away - its workspaces go to Not Listed, in the same order.'''
        for chip in list(card.chips.items):
            card.chips.take(chip)
            self.not_listed.chips.insert(chip, len(self.not_listed.chips.items))
            chip.zone = self.not_listed.chips
        self.section_list.take(card)
        self.category_list.take(card.chip)
        del self.cards[card.zone_id]
        for widget in (card, card.chip):
            widget.hide()
            widget.deleteLater()
        self.mark_dirty()

    def new_workspace(self, card: SectionCard):
        '''
        Asks for a new workspace's name and what to copy (see
        NewWorkspaceDialog) - the card's last workspace to begin with - and
        makes it in that card's category at once, at the bottom. It's
        written straight away (it needs its own folder), so the sorting
        changes still unsaved stay as they are - as with renaming and
        deleting one.
        '''
        templates = {chip.name: key for key, chip in sorted(self.chips.items(), key=lambda item: item[1].name)}
        template = card.chips.items[-1].key if card.chips.items else None
        category = card.section.get("category") if card.section is not None else None

        def create(name: str, folder: str, template_key: str):
            key = make_workspace(self.context, name, folder, template_key, {"category": category})
            self.workspaces[key] = self.raw_config(key)
            self.add_chip(key, card.chips)
            self.renumber()
            self.status_after(self.labels.get("workspace_sorter_created").format(name=name))
        NewWorkspaceDialog(self, self.context, templates, template, create).show()

    def rename_workspace(self, key: str):
        '''Asks for a new name and folder (see RenameWorkspaceDialog) and renames it at once - written straight away, like a new one.'''
        def rename(name: str, folder: str):
            new_key = rename_workspace(self.context, key, name, folder)
            chip = self.chips.pop(key)
            chip.key = new_key
            chip.set_name(name)
            self.chips[new_key] = chip
            self.workspaces[new_key] = self.raw_config(new_key)
            if new_key != key:
                del self.workspaces[key]
                # Already written to the select page (see relist_workspace) - so it's not a change to save
                for section in self.sections:
                    if section.get("workspace") == key:
                        section["workspace"] = new_key
            self.renumber()
            self.status_after(self.labels.get("workspace_sorter_renamed").format(name=name))
        RenameWorkspaceDialog(self, self.context, key, self.chips[key].name, rename).show()

    def delete_workspace(self, key: str):
        '''Deletes it for good, once its folder name's typed (see DeleteWorkspaceDialog) - written straight away.'''
        name = self.chips[key].name
        def delete():
            delete_workspace(self.context, key)
            chip = self.chips.pop(key)
            del self.workspaces[key]
            # Already gone from the select page (see relist_workspace)
            self.sections = [section for section in self.sections if section.get("workspace") != key]
            chip.zone.take(chip)
            chip.hide()
            chip.deleteLater()
            self.renumber()
            self.status_after(self.labels.get("workspace_sorter_deleted").format(name=name))
        DeleteWorkspaceDialog(self, self.context, key, name, delete).show()

    def status_after(self, done: str):
        '''Says something was written - and, with sorting still unsaved, that that still is.'''
        if self.dirty:
            self.set_status(f"{done} {self.labels.get('workspace_sorter_unsaved')}", "warning")
        else:
            self.set_status(done, "good")

    def edit_workspace(self, key: str):
        '''Opens the workspace editor on this workspace (Back returns here) - asking first if there are unsaved changes.'''
        def edit():
            # Imported here, like the select page's Edit This Workspace
            from .config_editor import ConfigEditor
            ConfigEditor.selected_key = key
            self.router.show("demo/config_editor")
        self.leave(edit)

    def open_workspace(self, key: str):
        '''Opens the workspace itself (Back returns here) - asking first if there are unsaved changes.'''
        self.leave(lambda: self.router.show(key))

    def leave(self, go):
        '''Calls go, which leaves this page - once confirmed, if there are unsaved changes.'''
        if not self.dirty:
            go()
            return
        modal.confirm_dialog(self, self.context, self.labels.get("workspace_sorter_discard_question"),
                             self.labels.get("workspace_sorter_discard_confirm"),
                             self.labels.get("workspace_sorter_discard_cancel"), go)

    # Dropping
    def drop_workspace(self, payload: DragPayload, zone: DropZone, index: int):
        chip = self.chips.get(payload.item_id)
        if chip is None:
            return
        self.move(chip, chip.zone, zone, index)
        chip.zone = zone
        self.mark_dirty()

    def drop_listed(self, payload: DragPayload, index: int):
        '''Something dropped among the categories: a category, or a workspace to go there on its own.'''
        if payload.kind == WORKSPACE:
            self.drop_workspace(payload, self.section_list, index)
        else:
            self.drop_section(payload, index, self.section_list)

    def drop_section(self, payload: DragPayload, index: int, zone: DropZone):
        '''
        A category dropped among the cards, or in the sidebar - where index
        counts categories only, so it lands just before the card it's
        dropped before there, after any workspaces on their own between them.
        '''
        card = self.cards.get(payload.item_id)
        if card is None or card is self.not_listed:
            return
        if zone is self.category_list:
            current = self.category_list.index_of(card.chip)
            if index in (current, current + 1):
                return  # dropped back where it was
            cards = [item for item in self.section_list.items if isinstance(item, SectionCard)]
            index = self.section_list.index_of(cards[index]) if index < len(cards) else len(self.section_list.items)
        if not self.move(card, self.section_list, self.section_list, index):
            return
        self.sync_sidebar()
        self.mark_dirty()

    def sync_sidebar(self):
        '''Puts the sidebar's chips in the cards' order.'''
        for position, card in enumerate(item for item in self.section_list.items if isinstance(item, SectionCard)):
            if self.category_list.index_of(card.chip) != position:
                self.category_list.take(card.chip)
                self.category_list.insert(card.chip, position)

    @staticmethod
    def move(widget: QWidget, source: DropZone, target: DropZone, index: int) -> bool:
        '''
        Moves widget from source to index in target - an index counted with
        it still in place, as a drop's slot is. False if that's where it
        already was.
        '''
        if source is target:
            current = source.index_of(widget)
            if index in (current, current + 1):
                return False  # dropped back where it was
            if index > current:
                index -= 1
        source.take(widget)
        target.insert(widget, index)
        return True

    def renumber(self):
        '''Numbers the shown workspaces in numbered categories, as the select page will - not ones on their own.'''
        for item in self.section_list.items:
            if isinstance(item, WorkspaceChip):
                item.number(None)
        for card in self.cards.values():
            numbered = card.section is not None and card.section.get("numbered", False)
            position = 0
            for chip in card.chips.items:
                if numbered and chip.shown.isChecked():
                    position += 1
                    chip.number(position)
                else:
                    chip.number(None)

    def mark_dirty(self):
        self.renumber()
        if not self.dirty:
            self.dirty = True
            self.set_status(self.labels.get("workspace_sorter_unsaved"), "warning")

    def set_status(self, text: str, tone: str):
        self.status.setText(text)
        self.style.set_tone(self.status, tone)

    # Saving
    def save(self):
        written = 0
        for card in self.cards.values():
            previous = (0, "")
            for chip in card.chips.items:
                config = self.workspaces[chip.key]
                changes = {"include": 1 if chip.shown.isChecked() else 0}
                if card.section is not None:
                    changes["category"] = card.section.get("category")
                    # Its own order if it still sorts after the one before it - by (order, key),
                    # as the select page sorts them - so moving one workspace only rewrites
                    # the ones it has to
                    order = self.number_or_zero(config.get("order"))
                    if (order, chip.key) <= previous:
                        order = previous[0] + 1
                    changes["order"] = order
                    previous = (order, chip.key)
                changes = {name: value for name, value in changes.items() if config.get(name) != value}
                if changes:
                    self.write_values(chip.key, changes)
                    config.update(changes)
                    written += 1

        # On their own: listed by the select page's sections, in no category
        for chip in self.section_list.items:
            if isinstance(chip, WorkspaceChip):
                config = self.workspaces[chip.key]
                changes = {name: value for name, value in (("include", 1 if chip.shown.isChecked() else 0), ("category", None))
                           if config.get(name) != value}
                if changes:
                    self.write_values(chip.key, changes)
                    config.update(changes)
                    written += 1

        sections = [copy.deepcopy(item.section) if isinstance(item, SectionCard) else {"workspace": item.key}
                    for item in self.section_list.items]
        for section in sections:
            if "workspace" in section:
                continue
            key = f"title_buttons_{section.get('label')}"
            if key in self.new_labels:
                self.labels.add_default_label(key, self.new_labels.pop(key), after_prefix="title_buttons_")
        self.new_labels.clear()  # what's left was for categories removed before they were saved
        if sections != self.sections:
            self.write_values(self.SELECT_PAGE, {"sections": sections})
            self.sections = sections
            written += 1

        self.dirty = False
        self.set_status(self.labels.get("workspace_sorter_saved").format(count=written), "good")

    def write_values(self, key: str, values: dict):
        '''Sets top-level values in a page's config.json, the rest of the file as it was (see write_config_values).'''
        write_config_values(self.context, key, values)
