import copy
import json
import re

from PySide6.QtWidgets import QCheckBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from ...app_core import Context
from ...widgets import MenuBar, Scrollable, popup
from ...widgets.frame_widgets.drag_drop import DragHandle, DragPayload, DropZone, ListZone
from ...widgets.frame_widgets.important_buttons import PAGE_MARK, POPUP_MARK
from ..page import Page
from .config_editor import NewWorkspaceDialog, make_workspace

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
    faded - and a link to edit it in the workspace editor.
    '''

    def __init__(self, context: Context, key: str, name: str, shown: bool, changed, edit):
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
        editor = QPushButton(f"{context.labels.get('workspace_sorter_edit_workspace')} {PAGE_MARK}")
        editor.setFont(context.style.get_font("default"))
        editor.setToolTip(context.labels.get("workspace_sorter_edit_workspace_tooltip"))
        editor.clicked.connect(lambda checked=False: edit(self.key))
        layout.addWidget(editor)
        self.show_state()
        DragHandle(self, lambda: DragPayload(WORKSPACE, self.key, self.zone.zone_id))

    def number(self, position: int | None):
        '''Shows its place in a numbered section - as the select page numbers it - or just its name.'''
        self.label.setText(self.name if position is None else f"{position}. {self.name}")

    def show_state(self):
        self.style.set_tone(self.label, None if self.shown.isChecked() else "muted")


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


class WorkspaceSorter(Page):
    '''
    Developer page for sorting and categorizing workspaces - what the
    workspace select page lists, under which section, in which order -
    by dragging instead of editing each workspace's config. One column:

      - Each category - a select page section (title/select_workspace's
        "sections") - is a card listing its workspaces top to bottom. Drag
        a workspace within a card to reorder it, or onto another card to
        move it to that category ("category").
      - Drag a card by its title to reorder the categories. Its Numbered
        checkbox numbers its workspaces on the select page, Shown lists
        the whole category there or not ("hidden"), and Remove takes it
        away - its workspaces go to Not Listed.
      - Each workspace's Shown checkbox is its "include" - a hidden one
        keeps its place, for whenever it's shown again - and its Edit
        button opens it in the workspace editor.
      - Add Category, under the cards, adds an empty one with the name
        typed beside it.
      - Workspaces whose category no section lists sit in Not Listed at
        the bottom - drag one into a category to list it.
      - New Workspace, under each card, makes a workspace in it right
        away (see make_workspace) - in Not Listed, with no category.

    Nothing is written until Save, which sets every workspace's
    "category", "order" and "include" in its config.json - only the files
    that change - and the categories in title/select_workspace's
    config.json, adding a new category's name to the labels. Discard
    Changes rebuilds the page from the files.
    '''

    SELECT_PAGE = "title/select_workspace"
    NOT_LISTED = "_not_listed"
    COLUMN_WIDTH = 820

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

        scrollable = Scrollable(self, context)
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

        self.section_list = ListZone(context, "sections", {SECTION})
        self.section_list.dropped.connect(self.drop_section)
        column_layout.addWidget(self.section_list)

        self.cards: dict[str, SectionCard] = {}
        for section in self.sections:
            self.add_section(copy.deepcopy(section), self.labels.get(f'title_buttons_{section.get("label", "_default")}'))

        column_layout.addWidget(self.build_new_category_row())

        # Only ever dragged out of - a workspace is listed by being in a category
        self.not_listed = SectionCard(self, self.NOT_LISTED, self.labels.get("workspace_sorter_not_listed"), None,
                                      self.labels.get("workspace_sorter_not_listed_note"))
        self.cards[self.NOT_LISTED] = self.not_listed
        column_layout.addWidget(self.not_listed)

        self.chips: dict[str, WorkspaceChip] = {}
        ordered = sorted(self.workspaces.items(), key=lambda item: (self.number_or_zero(item[1].get("order")), item[0]))
        for key, config in ordered:
            self.add_chip(key, self.cards.get(self.zone_id(config.get("category")), self.not_listed))
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

    def add_chip(self, key: str, card: SectionCard):
        '''A chip for workspace key, at the bottom of card.'''
        chip = WorkspaceChip(self.context, key, self.labels.get(self.pages.link_label(key)),
                             self.workspaces[key].get("include") == 1, self.mark_dirty, self.edit_workspace)
        self.chips[key] = chip
        chip.zone = card.chips
        card.chips.insert(chip, len(card.chips.items))

    # Categories
    def add_section(self, section: dict, title: str) -> SectionCard:
        '''A card for section, at the bottom of the list, draggable by its header.'''
        card = SectionCard(self, self.zone_id(section.get("category")), title, section)
        card.chips.dropped.connect(lambda payload, slot, zone=card.chips: self.drop_workspace(payload, zone, slot))
        self.cards[card.zone_id] = card
        self.section_list.insert(card, len(self.section_list.items))
        DragHandle(card.header, lambda: DragPayload(SECTION, card.zone_id, self.section_list.zone_id), preview=card)
        return card

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
        del self.cards[card.zone_id]
        card.hide()
        card.deleteLater()
        self.mark_dirty()

    def new_workspace(self, card: SectionCard):
        '''
        Asks for a new workspace's name and what to copy (see
        NewWorkspaceDialog) - the card's last workspace to begin with - and
        makes it in that card's category at once, at the bottom. It's
        written straight away (it needs its own folder), so the sorting
        changes still unsaved stay as they are.
        '''
        templates = {chip.name: key for key, chip in sorted(self.chips.items(), key=lambda item: item[1].name)}
        template = card.chips.items[-1].key if card.chips.items else None
        category = card.section.get("category") if card.section is not None else None

        def create(name: str, folder: str, template_key: str):
            key = make_workspace(self.context, name, folder, template_key, {"category": category})
            self.workspaces[key] = self.raw_config(key)
            self.add_chip(key, card)
            self.renumber()
            created = self.labels.get("workspace_sorter_created").format(name=name)
            if self.dirty:  # still unsaved, and the status line is where that shows
                self.set_status(f"{created} {self.labels.get('workspace_sorter_unsaved')}", "warning")
            else:
                self.set_status(created, "good")
        NewWorkspaceDialog(self, self.context, templates, template, create).show()

    def edit_workspace(self, key: str):
        '''Opens the workspace editor on this workspace (Back returns here) - asking first if there are unsaved changes.'''
        def edit():
            # Imported here, like the select page's Edit This Workspace
            from .config_editor import ConfigEditor
            ConfigEditor.selected_key = key
            self.router.show("demo/config_editor")
        if not self.dirty:
            edit()
            return
        popup.confirm_dialog(self, self.context, self.labels.get("workspace_sorter_discard_question"),
                             self.labels.get("workspace_sorter_discard_confirm"),
                             self.labels.get("workspace_sorter_discard_cancel"), edit)

    # Dropping
    def drop_workspace(self, payload: DragPayload, zone: DropZone, index: int):
        chip = self.chips.get(payload.item_id)
        if chip is None:
            return
        self.move(chip, chip.zone, zone, index)
        chip.zone = zone
        self.mark_dirty()

    def drop_section(self, payload: DragPayload, index: int):
        card = self.cards.get(payload.item_id)
        if card is None or card is self.not_listed:
            return
        self.move(card, self.section_list, self.section_list, index)
        self.mark_dirty()

    @staticmethod
    def move(widget: QWidget, source: DropZone, target: DropZone, index: int):
        '''Moves widget from source to index in target - an index counted with it still in place, as a drop's slot is.'''
        if source is target:
            current = source.index_of(widget)
            if index in (current, current + 1):
                return  # dropped back where it was
            if index > current:
                index -= 1
        source.take(widget)
        target.insert(widget, index)

    def renumber(self):
        '''Numbers the shown workspaces in numbered categories, as the select page will.'''
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

        sections = [copy.deepcopy(card.section) for card in self.section_list.items]
        for section in sections:
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

    # A top-level key's line in a config written 4-space indented (see Json.format_config)
    TOP_LEVEL_KEY = r'^    "{}"\s*:\s*'

    def write_values(self, key: str, values: dict):
        '''
        Sets top-level values in a page's config.json by rewriting only
        those values in its text, so the rest of the hand-written file -
        its blank lines, its one-line lists - stays exactly as it was.
        A key it doesn't have yet is added at the end.
        '''
        path = self.pages.config_paths[key]
        text = path.read_text(encoding="utf-8")
        json_tools = self.context.json
        for name, value in values.items():
            formatted = json_tools.format_value(value, 4)
            match = re.search(self.TOP_LEVEL_KEY.format(re.escape(name)), text, re.MULTILINE)
            if match is not None:
                _, end = json.JSONDecoder().raw_decode(text, match.end())
                text = text[:match.end()] + formatted + text[end:]
            else:
                close = text.rstrip().rfind("}")
                body = text[:close].rstrip()
                text = f"{body},\n    {json.dumps(name)}: {formatted}\n}}\n"
        json.loads(text)  # never write a broken config
        path.write_text(text, encoding="utf-8")
