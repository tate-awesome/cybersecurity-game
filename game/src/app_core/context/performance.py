import re
import time
from collections import deque

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFontDatabase, QPainter
from PySide6.QtWidgets import QApplication, QLabel

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Context

# How often the shared AnimationManager ticks - every data panel's refresh
# and every canvas repaint rides on it, so this is the app's main framerate.
# 10 matches the old fixed 100 ms tick.
DEFAULT_UI_FPS = 10
UI_FPS_RANGE = (1, 60)
DEFAULT_ANTIALIASING = True
DEFAULT_PAGE_TRANSITIONS = True
DEFAULT_PERFORMANCE_OVERLAY = False
DEFAULT_PERFORMANCE_LOG = False

# One-click bundles of the settings that cost the most - the Performance
# tab's preset dropdown. Background keys are handed to Style.set_background.
QUALITY_PRESETS: dict[str, dict] = {
    "low": {"ui_fps": 5, "antialiasing": False, "page_transitions": False,
            "background_fps": 10, "background_animate": False},
    "balanced": {"ui_fps": DEFAULT_UI_FPS, "antialiasing": True, "page_transitions": True,
                 "background_fps": 30, "background_animate": True},
    "high": {"ui_fps": 30, "antialiasing": True, "page_transitions": True,
             "background_fps": 60, "background_animate": True},
}

# A callback or widget name's trailing "_<id(self)>" - stripped so every
# instance of one kind of widget is measured together
INSTANCE_SUFFIX = re.compile(r"_\d+$")


class Meter:
    '''
    Timestamped samples (in ms) from the last `window` seconds - enough
    for a rate (samples per second), an average and a peak.
    '''

    def __init__(self, window: float = 2.0):
        self.window = window
        self.samples: deque[tuple[float, float]] = deque()

    def add(self, value: float, now: float):
        self.samples.append((now, value))
        self.prune(now)

    def prune(self, now: float):
        while self.samples and now - self.samples[0][0] > self.window:
            self.samples.popleft()

    def rate(self) -> float:
        return len(self.samples) / self.window

    def average(self) -> float:
        return sum(value for _, value in self.samples) / len(self.samples) if self.samples else 0.0

    def peak(self) -> float:
        return max((value for _, value in self.samples), default=0.0)

    def total(self) -> float:
        return sum(value for _, value in self.samples)


class Performance:
    '''
    Performance settings, and measurements of how the app is keeping up.

    Settings (saved as preferences, like Style's): the UI framerate (the
    shared AnimationManager's tick), antialiasing on canvases and the
    background, page transitions, and the two ways to see measurements -
    an on-screen overlay (also F3) and console logging.

    Measurements are only taken while one of those is on (`measuring`),
    so they cost nothing otherwise:
      tick        - each AnimationManager pass: how long it took, and how
                    many happened a second (its achieved framerate)
      late        - how far past its due time each tick ran - the main
                    thread being busy shows up here as jank
      callback:*  - each animation callback's share of the tick, by kind
      paint:*     - each canvas kind's paintEvent (repaints are only
                    scheduled by the tick, so they're timed separately)
      background  - each freshly rendered background frame
    plus each page's build time and app startup (see Router.show / App).
    '''

    def __init__(self, context: "Context"):
        self.context = context
        self.meters: dict[str, Meter] = {}
        self._groups: dict[str, str] = {}
        self.page: str | None = None
        self.page_build_ms: float | None = None
        self.page_ready_ms: float | None = None
        self.startup_ms: float | None = None
        self.overlay: QLabel | None = None
        self._overlay_timer = QTimer()
        self._overlay_timer.setInterval(500)
        self._overlay_timer.timeout.connect(self.update_overlay)
        self.load_defaults()
        self.load()

    # Settings
    PREFERENCES = {
        # attribute: (preference key, type)
        "ui_fps": ("ui_fps", int),
        "antialiasing": ("antialiasing", bool),
        "page_transitions": ("page_transitions", bool),
        "overlay_enabled": ("performance_overlay", bool),
        "log_enabled": ("performance_log", bool),
    }

    def load_defaults(self):
        '''Back to the DEFAULT_* values, without saving - like Style.load_default_background.'''
        self.ui_fps: int = DEFAULT_UI_FPS
        self.antialiasing: bool = DEFAULT_ANTIALIASING
        self.page_transitions: bool = DEFAULT_PAGE_TRANSITIONS
        self.overlay_enabled: bool = DEFAULT_PERFORMANCE_OVERLAY
        self.log_enabled: bool = DEFAULT_PERFORMANCE_LOG

    def load(self):
        '''Reads the saved settings, keeping the default for anything missing or invalid.'''
        preferences = self.context.preferences
        for attribute, (key, kind) in self.PREFERENCES.items():
            value = preferences.get(key)
            if kind is int and isinstance(value, (int, float)) and not isinstance(value, bool):
                value = int(value)
            if isinstance(value, kind):
                setattr(self, attribute, value)
        self.ui_fps = min(UI_FPS_RANGE[1], max(UI_FPS_RANGE[0], self.ui_fps))

    def save(self):
        for attribute, (key, _kind) in self.PREFERENCES.items():
            self.context.preferences.set(key, getattr(self, attribute))

    def reset(self):
        '''Every setting back to its default, saved and applied.'''
        self.load_defaults()
        self.save()
        self.apply()

    def set(self, ui_fps: int | None = None, antialiasing: bool | None = None, page_transitions: bool | None = None,
            overlay: bool | None = None, log: bool | None = None):
        '''Changes settings - applied at once, and saved.'''
        if ui_fps is not None:
            self.ui_fps = min(UI_FPS_RANGE[1], max(UI_FPS_RANGE[0], int(ui_fps)))
        if antialiasing is not None:
            self.antialiasing = antialiasing
        if page_transitions is not None:
            self.page_transitions = page_transitions
        if overlay is not None:
            self.overlay_enabled = overlay
        if log is not None:
            self.log_enabled = log
        self.save()
        self.apply()

    def apply(self):
        '''Brings the running app in line with the settings - no page rebuild needed.'''
        manager = getattr(self.context, "animation_manager", None)
        if manager is not None:
            manager.set_frame_time(self.ui_frame_ms())
        if not self.measuring:
            self.meters.clear()
        self.show_overlay(self.overlay_enabled)
        # Still canvases only repaint when asked - antialiasing shows at once
        for window in QApplication.topLevelWidgets():
            if window.isVisible():
                window.update()

    def toggle_overlay(self):
        self.set(overlay=not self.overlay_enabled)

    def ui_frame_ms(self) -> int:
        return max(1, round(1000 / self.ui_fps))

    # Presets
    def apply_preset(self, name: str):
        preset = QUALITY_PRESETS[name]
        self.set(ui_fps=preset["ui_fps"], antialiasing=preset["antialiasing"],
                 page_transitions=preset["page_transitions"])
        self.context.style.set_background(fps=preset["background_fps"], animate=preset["background_animate"])

    def current_preset(self) -> str:
        '''The preset every relevant setting currently matches, or "" for a custom mix.'''
        style = self.context.style
        current = {"ui_fps": self.ui_fps, "antialiasing": self.antialiasing, "page_transitions": self.page_transitions,
                   "background_fps": style.background_fps, "background_animate": style.background_animate}
        for name, preset in QUALITY_PRESETS.items():
            if preset == current:
                return name
        return ""

    # Rendering
    def apply_render_hints(self, painter: QPainter):
        '''Antialiasing for a canvas's painter, as the setting says.'''
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, self.antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, self.antialiasing)

    # Measuring
    @property
    def measuring(self) -> bool:
        return self.overlay_enabled or self.log_enabled

    def group(self, name: str) -> str:
        '''A callback/widget name without its per-instance id suffix - cached, since it's asked every tick.'''
        group = self._groups.get(name)
        if group is None:
            group = self._groups[name] = INSTANCE_SUFFIX.sub("", name)
        return group

    def record(self, name: str, started: float, now: float | None = None):
        '''Adds a sample to `name`'s meter: the ms since `started` (a time.perf_counter() reading).'''
        now = time.perf_counter() if now is None else now
        self.record_value(name, (now - started) * 1000, now)

    def record_value(self, name: str, value_ms: float, now: float | None = None):
        meter = self.meters.get(name)
        if meter is None:
            meter = self.meters[name] = Meter()
        meter.add(value_ms, time.perf_counter() if now is None else now)

    def page_started(self) -> float:
        return time.perf_counter()

    def page_built(self, page: str, started: float):
        '''
        Called once a page's widgets exist: records the build time, then
        once more when the event loop next comes round (after the first
        layout and paint have been queued and handled) as "ready".
        '''
        self.page = page
        self.page_build_ms = (time.perf_counter() - started) * 1000
        self.page_ready_ms = None

        def ready():
            if self.page != page:
                return
            self.page_ready_ms = (time.perf_counter() - started) * 1000
            if self.log_enabled:
                print(f"[Performance] page {page!r}: built in {self.page_build_ms:.0f} ms, ready in {self.page_ready_ms:.0f} ms")
        QTimer.singleShot(0, ready)

    def app_started(self):
        '''Called by App once the first page is up - from the first app import (see src/__init__.py) to now.'''
        from ... import STARTED
        self.startup_ms = (time.perf_counter() - STARTED) * 1000
        if self.log_enabled:
            print(f"[Performance] startup: {self.startup_ms:.0f} ms")
        self.apply()

    # Report
    def report(self) -> list[str]:
        '''The measurements so far, one line each - for the overlay and the console log.'''
        now = time.perf_counter()
        for meter in self.meters.values():
            meter.prune(now)
        lines = []
        tick = self.meters.get("tick")
        late = self.meters.get("late")
        if tick is not None and tick.samples:
            lines.append(f"UI tick     {tick.rate():5.1f} / {self.ui_fps} fps   "
                         f"{tick.average():5.2f} ms avg  {tick.peak():5.2f} max")
        if late is not None and late.samples:
            lines.append(f"Late by     {late.average():5.1f} ms avg  {late.peak():5.1f} max")
        callbacks = sorted(((name.split(":", 1)[1], meter) for name, meter in self.meters.items()
                            if name.startswith("callback:") and meter.samples),
                           key=lambda item: item[1].total(), reverse=True)
        if callbacks:
            lines.append(f"Callbacks   {len(self.context.animation_manager.callbacks)} registered, slowest:")
            for name, meter in callbacks[:4]:
                lines.append(f"  {name[:30]:30} {meter.average():5.2f} ms avg  {meter.peak():5.2f} max")
        paints = sorted(((name.split(":", 1)[1], meter) for name, meter in self.meters.items()
                         if name.startswith("paint:") and meter.samples),
                        key=lambda item: item[1].total(), reverse=True)
        if paints:
            lines.append("Paint")
            for name, meter in paints[:4]:
                lines.append(f"  {name[:22]:22} {meter.rate():5.1f}/s  {meter.average():5.2f} ms avg  {meter.peak():5.2f} max")
        background = self.meters.get("background")
        if background is not None and background.samples:
            lines.append(f"Background  {background.rate():5.1f} fps   {background.average():5.2f} ms avg  {background.peak():5.2f} max")
        if self.page_build_ms is not None:
            ready = f"{self.page_ready_ms:.0f}" if self.page_ready_ms is not None else "..."
            lines.append(f"Page        built {self.page_build_ms:.0f} ms, ready {ready} ms")
        if self.startup_ms is not None:
            lines.append(f"Startup     {self.startup_ms / 1000:.2f} s")
        return lines or ["Measuring..."]

    # Overlay
    def show_overlay(self, show: bool):
        if show:
            if self.overlay is None:
                self.overlay = QLabel(self.context.root)
                self.overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
                font = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
                font.setPointSize(9)
                self.overlay.setFont(font)
                # Fixed colors, not the theme's - it has to read over anything
                self.overlay.setStyleSheet("QLabel { background-color: rgba(0, 0, 0, 170); color: #7CFC9A;"
                                           " padding: 6px; border-radius: 4px; }")
            self.update_overlay()
            self.overlay.show()
        elif self.overlay is not None:
            self.overlay.hide()
        # The same timer drives the console log
        if self.measuring:
            self._overlay_timer.start()
        else:
            self._overlay_timer.stop()

    def update_overlay(self):
        lines = self.report()
        if self.overlay is not None and self.overlay_enabled:
            self.overlay.setText("\n".join(lines))
            self.overlay.adjustSize()
            root = self.context.root
            self.overlay.move(root.width() - self.overlay.width() - 12, 48)
            self.overlay.raise_()  # above a page built since
        if self.log_enabled:
            self._log_lines(lines)

    _last_log = 0.0

    def _log_lines(self, lines: list[str]):
        '''Prints the report every few seconds, rather than on every overlay update.'''
        now = time.perf_counter()
        if now - self._last_log < 5.0:
            return
        self._last_log = now
        print("[Performance]\n  " + "\n  ".join(lines))
