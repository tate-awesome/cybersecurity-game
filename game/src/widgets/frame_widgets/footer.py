import html
import time

from PySide6.QtCore import QEvent, QObject, Qt, QTimer
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QMainWindow

from ...app_core import Context
from ...app_core.version import BuildInfo
from ...network.hardware import Wifi
from .important_buttons import DEVELOPER_MARK

# Seconds between the footer's updates, and how many updates apart the
# slower readings are taken
TICK_MS = 1000
WIFI_EVERY = 3
SAVED_NETWORKS_EVERY = 30

# Whether the footer has no background of its own, so the page (and its
# background visual) shows through - a preference, set on the settings page
DEFAULT_FOOTER_TRANSPARENT = False


class _Quiet:
    '''
    Stands in for the Buffer for the footer's own Wifi: it only reads the
    current and saved networks, and a reading that can't be taken (no
    Wi-Fi device, service not running) just shows as "not connected" -
    not a status console message every few seconds.
    '''
    def put(self, *args, **kwargs):
        pass


class _FollowResize(QObject):
    '''Calls back whenever the window resizes - the footer isn't in a layout, so it moves itself.'''
    def __init__(self, window: QMainWindow, callback):
        super().__init__(window)
        self.callback = callback
        window.installEventFilter(self)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.Resize:
            self.callback()
        return False


class Footer(QFrame):
    '''
    The bar along the bottom of the window, on every page. It belongs to
    the main window rather than to a page, so it stays put while pages
    change - Router calls page_changed after each page is built (a theme
    or zoom change rebuilds the page, so that's when it restyles too).

    It floats over the bottom of the page rather than sitting below it,
    and each page gets that much more bottom margin so nothing of its own
    is covered - only its background runs underneath, which is what a
    transparent footer (see set_transparent) shows.

    Left to right: where you are (the navigation history on hover), the
    Wi-Fi network (saved networks on hover), the theme (the rest of the
    appearance settings on hover) | developer mode, the UI
    framerate, zoom (keybinds on hover), session time, and the version.

    It keeps its own slow timer, since each page's AnimationManager is
    torn down with the page. Every reading is cheap: the framerate is a
    tick count (see Performance.ticks), and Wi-Fi is asked every few
    seconds, not every frame.
    '''

    def __init__(self, root: QMainWindow, context: Context):
        super().__init__(root)
        self.root = root
        self.context = context
        self.style = context.style
        self.labels = context.labels
        self.setObjectName(f"_footer_{id(self)}")
        # Not a surface: never frosted or tinted (see app_core.context.backdrop)
        self.setProperty("surface", "none")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.row = QHBoxLayout(self)
        self.row.setContentsMargins(0, 0, 0, 0)
        self.row.setSpacing(0)
        self.transparent = self.preferred_transparent()
        self.held = False  # see hold
        self._placer = _FollowResize(root, self.place)

        self.build = BuildInfo(context.paths.assets)
        self.wifi = Wifi(_Quiet(), context)
        self.ssid: str | None = None
        self.saved_networks: list[str] = []
        self.updates = 0
        self.last_ticks = context.performance.ticks
        self.last_tick_time = time.perf_counter()
        from ... import STARTED
        self.started = STARTED
        self.started_clock = time.time() - (time.perf_counter() - STARTED)

        self.location = self._item()
        self.wifi_label = self._item()
        self.theme = self._item()
        self.row.addStretch()
        self.developer = self._item()
        self.fps = self._item()
        self.zoom = self._item()
        self.session = self._item()
        self.version = self._item()
        # Styled by these (see restyle) - set before the stylesheet polishes them
        self.location.setProperty("first", True)
        self.developer.setProperty("badge", True)

        self.timer = QTimer(self)
        self.timer.setInterval(TICK_MS)
        self.timer.timeout.connect(self.update_live)
        self.timer.start()

        self.update_saved_networks()
        self.page_changed()

    def _item(self) -> QLabel:
        '''The next label along the bar.'''
        label = QLabel()
        label.setTextFormat(Qt.TextFormat.PlainText)
        self.row.addWidget(label)
        return label

    def label(self, key: str) -> str:
        return self.labels.get(f"footer_{key}")

    # Placement
    def place(self):
        '''Along the bottom of the window, above the page.'''
        height = self.sizeHint().height()
        self.setGeometry(0, self.root.height() - height, self.root.width(), height)
        # Made after the window was shown, so it starts hidden - and not
        # shown before the first page, which it comes in with (see App)
        if self.context.router.current_frame is not None and not self.held:
            self.show()
            self.raise_()

    def hold(self):
        '''Hidden until release() - while the first page waits to come in (see App.hold_first_page).'''
        self.held = True
        self.hide()

    def release(self):
        self.held = False
        self.place()

    def pad_page(self):
        '''
        Gives the page showing now enough extra bottom margin that the
        footer covers none of its content. Once per page - a page is
        built fresh on every show, refresh included.
        '''
        page = self.root.centralWidget()
        if page is None or page.property("footer_padded"):
            return
        margins = page.contentsMargins()
        page.setContentsMargins(margins.left(), margins.top(), margins.right(),
                                margins.bottom() + self.sizeHint().height())
        page.setProperty("footer_padded", True)

    def preferred_transparent(self) -> bool:
        transparent = self.context.preferences.get("footer_transparent")
        return transparent if isinstance(transparent, bool) else DEFAULT_FOOTER_TRANSPARENT

    def load_preferences(self):
        '''Back in line with preferences (see Context.reload_preferences).'''
        self.transparent = self.preferred_transparent()
        self.restyle()

    def set_transparent(self, transparent: bool):
        '''Drops (or brings back) the footer's background - applied at once, and saved.'''
        self.transparent = transparent
        self.context.preferences.set("footer_transparent", transparent)
        self.restyle()

    # Updates
    def page_changed(self):
        '''After every page build: the theme, zoom and labels may have changed with it.'''
        self.restyle()
        self.place()
        self.pad_page()
        # Tooltips that are otherwise only built once - the labels may be new
        for label in (self.zoom, self.session, self.version):
            label.setToolTip("")
        self.fps.setToolTip(tooltip([self.label("tooltips_fps")]))
        self.update_location()
        self.update_developer()
        self.update_live()

    def restyle(self):
        style = self.style
        size = max(6, round(12 * style.ui_scale / 100.0))
        self.setFont(QFont("Arial", size))
        for label in self.findChildren(QLabel):
            label.setFont(self.font())
        text = QColor(style.color("text"))
        faint = QColor(text)
        faint.setAlpha(70)
        faint = faint.name(QColor.NameFormat.HexArgb)
        name = self.objectName()
        if self.transparent:
            background = "background: transparent; border: none;"
        else:
            background = f"background-color: {style.color('widget', opaque=True)}; border-top: 1px solid {faint};"
        self.setStyleSheet(style.themed(
            f"QFrame#{name} {{ {background} }}"
            f" QFrame#{name} QLabel {{ color: {text.name()}; background: transparent;"
            f" padding: 2px {style.igap}px; border: none; border-left: 1px solid {faint}; }}"
            f" QFrame#{name} QLabel[first=\"true\"] {{ border-left: none; }}"
            f" QFrame#{name} QLabel[badge=\"true\"] {{ color: {style.color('accent')}; font-weight: bold; }}",
            opaque=True))

    def update_live(self):
        '''Every second: the readings that change by themselves.'''
        self.update_session()
        self.update_fps()
        self.update_zoom()  # fullscreen changes without a rebuild (F11)
        self.update_theme()  # translucency and the background change without a rebuild
        if self.updates % WIFI_EVERY == 0:
            self.update_wifi()
        if self.updates % SAVED_NETWORKS_EVERY == 0 and self.updates > 0:
            self.update_saved_networks()
        self.update_version()
        self.updates += 1

    # Location
    def page_name(self, key: str) -> str:
        '''A page's name as its links show it, or its own footer label, or just its key.'''
        config = self.context.pages.load_page_config(key)
        label_key = config.get("link_label") if isinstance(config.get("link_label"), str) else f"footer_pages_{key}"
        try:
            return self.labels.get(label_key)
        except KeyError:
            return key

    def update_location(self):
        router = self.context.router
        stack = list(router.navigation_stack)
        current = stack[-1] if stack else (router.current_page or "")
        set_text(self.location, self.page_name(current))
        lines = [self.label("tooltips_location")]
        for depth, key in enumerate(stack):
            marker = "▸ " if depth == len(stack) - 1 else " "
            lines.append(f"{marker}{'  ' * depth}{self.page_name(key)}")
        self.location.setToolTip(tooltip(lines))

    # Wi-Fi
    def page_wifi(self) -> Wifi | None:
        '''This page's own Wi-Fi process (the Wi-Fi form's), if it has one.'''
        for process in self.context.process_manager.processes.values():
            if isinstance(process, Wifi):
                return process
        return None

    def update_wifi(self):
        page_wifi = self.page_wifi()
        # While the page is switching networks, the OS Wi-Fi APIs are left to
        # it (on Linux they can't be used from two threads at once - see
        # WifiBaseClass.start); the last reading stands until it's done
        if page_wifi is None or not page_wifi._connecting:
            self.ssid = self.wifi.get_current_ssid()

        name = self.ssid if self.ssid is not None else self.label("wifi_none")
        set_text(self.wifi_label, f"{self.label('wifi')}: {name}")

        if self.ssid is not None:
            lines = [f"{self.label('tooltips_wifi_current')} {self.ssid}"]
        else:
            lines = [self.label("tooltips_wifi_disconnected")]
        if page_wifi is not None and page_wifi.is_connected and page_wifi.previous_network:
            lines.append(f"{self.label('tooltips_wifi_restore')} {page_wifi.previous_network}")
        lines.append("")
        lines.append(self.label("tooltips_wifi_saved"))
        if self.saved_networks:
            for network in self.saved_networks:
                current = self.ssid is not None and network.lower() == self.ssid.lower()
                lines.append(f"{chr(0x25cf) if current else chr(0x2003)} {network}")
        else:
            lines.append(f" {self.label('tooltips_wifi_none_saved')}")
        self.wifi_label.setToolTip(tooltip(lines))

    def update_saved_networks(self):
        page_wifi = self.page_wifi()
        if page_wifi is not None and page_wifi._connecting:
            return
        self.saved_networks = sorted(set(self.wifi.get_network_history()), key=str.lower)

    # Theme
    def update_theme(self):
        '''
        The theme as "<mode> <hierarchy> <accent>" - e.g. "dark baseline
        teal", or "dark special kimbie" for a special theme, which has no
        hierarchy of its own - with every appearance setting on hover.
        '''
        style = self.style
        mode = self.labels.get(f"settings_page_mode_{style.current_theme.partition('_')[0]}")
        special = style.is_preset()
        if special:
            family = style.theme_family()
            hierarchy = self.label("theme_special")
            accent = style.preset_info.get(family, {}).get("label", family.replace("_", " "))
        else:
            hierarchy = style.theme_hierarchy.replace("_", " ")
            accent = style.theme_accent.replace("_", " ")
        mode, hierarchy, accent = mode.lower(), hierarchy.lower(), accent.lower()
        set_text(self.theme, f"{mode} {hierarchy} {accent}")

        def on_off(on: bool) -> str:
            return self.label("on" if on else "off")
        lines = [
            self.label("tooltips_theme"),
            f"{self.label('theme_mode')}: {mode}",
            f"{self.label('theme_hierarchy')}: {hierarchy}",
            f"{self.label('theme_accent')}: {accent}",
        ]
        if not special:  # special themes have their own colors - tint does nothing to them
            lines.append(f"{self.label('theme_tint')}: {round(style.theme_tint * 100)}%")
        background = self.labels.get(f"visual_names_{style.background_visual}") if style.background_enabled else self.label("off")
        lines += [
            f"{self.label('theme_inset')}: {on_off(style.theme_inset)}",
            f"{self.label('theme_invert')}: {on_off(style.invert_buttons)}",
            f"{self.label('theme_translucency')}: {on_off(style.translucent_surfaces)}",
            f"{self.label('theme_background')}: {background}",
        ]
        self.theme.setToolTip(tooltip(lines))

    # Developer mode
    def update_developer(self):
        developer = self.context.preferences.is_developer()
        debug_labels = self.labels.is_debug()
        parts = []
        lines = []
        if developer:
            parts.append(f"{DEVELOPER_MARK} {self.label('developer')}")
            lines.append(self.label("tooltips_developer"))
        if debug_labels:
            parts.append(self.label("debug_labels"))
            lines.append(self.label("tooltips_debug_labels"))
        set_text(self.developer, " · ".join(parts))
        self.developer.setToolTip(tooltip(lines))
        self.developer.setVisible(bool(parts))

    # Framerate
    def update_fps(self):
        performance = self.context.performance
        now = time.perf_counter()
        elapsed = now - self.last_tick_time
        if elapsed <= 0:
            return
        achieved = (performance.ticks - self.last_ticks) / elapsed
        self.last_ticks = performance.ticks
        self.last_tick_time = now
        set_text(self.fps, f"{achieved:.0f}/{performance.ui_fps} {self.label('fps')}")

    # Zoom
    def update_zoom(self):
        text = f"{self.label('zoom')} {self.style.ui_scale:.0f}%"
        if self.context.root.isFullScreen():
            text += f" · {self.label('fullscreen')}"
        set_text(self.zoom, text)
        # Rebuilt each time, since keybinds can be changed on the settings page
        lines = [f"{keys}    {self.label(f'keybinds_{action}')}" for keys, action in self.context.keybinds.describe()]
        self.zoom.setToolTip(tooltip([self.label("tooltips_keybinds"), *lines]))

    # Session time
    def update_session(self):
        seconds = int(time.perf_counter() - self.started)
        hours, rest = divmod(seconds, 3600)
        minutes, seconds = divmod(rest, 60)
        set_text(self.session, f"{self.label('session')} {hours}:{minutes:02}:{seconds:02}")
        if not self.session.toolTip():
            started = time.strftime("%H:%M", time.localtime(self.started_clock))
            self.session.setToolTip(tooltip([f"{self.label('tooltips_session')} {started}"]))

    # Version
    def update_version(self):
        build = self.build
        text = f"v{build.version}"
        if build.commit is not None:
            text += f" · {build.commit}{'*' if build.dirty else ''}"
        if not set_text(self.version, text) and self.version.toolTip():
            return
        lines = [f"{self.label('tooltips_version')} {build.version}"]
        if build.commit is not None:
            commit = build.commit
            if build.dirty:
                commit += f" ({self.label('tooltips_dirty')})"
            lines.append(f"{self.label('tooltips_commit')} {commit}")
        if build.branch:
            lines.append(f"{self.label('tooltips_branch')} {build.branch}")
        if build.built:
            lines.append(f"{self.label('tooltips_built')} {build.built}")
        self.version.setToolTip(tooltip(lines))


def set_text(label: QLabel, text: str) -> bool:
    '''Sets a label's text only if it changed (a change relays out the bar) - returns whether it did.'''
    if label.text() == text:
        return False
    label.setText(text)
    return True


def tooltip(lines: list[str]) -> str:
    '''Lines as a rich-text tooltip, escaped - network and page names are never markup.'''
    return "<qt>" + "<br>".join(html.escape(line).replace("  ", "&nbsp;&nbsp;") for line in lines) + "</qt>"
