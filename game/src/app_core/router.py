from PySide6.QtWidgets import QApplication, QMainWindow, QWidget

from . import Context
from .transitions import FadeOut, PageTransition

# Import page builder objects here
# /demo
from ..pages.demo.sprites import Sprites
from ..pages.demo.boat_motion import BoatMotion
from ..pages.demo.triangle import Triangle
from ..pages.demo.visuals import Visuals
from ..pages.demo.config_editor import ConfigEditor

# /attacker
from ..pages.attacker.attacker import AttackerV0
from ..pages.defender.defender import DefenderV0

# /settings
from ..pages.settings import SettingsPage
from ..pages.theme_editor import ThemeEditorPage

# /generic (data-driven pages, dispatched by each page's own config "build_type").
# start and title/select_demo are build_type "title" pages
# and title/select_workspace is "workspace_select", all discovered below - no
# hand-written entries needed for them.
from ..pages.generic import WorkspacePage, TitlePage, WorkspaceSelectPage

# Hard-coded 404 page - needs nothing from assets/, so it still works without it
from ..pages.not_found import NotFound

# The bar along the bottom of the window - outlives every page
from ..widgets.frame_widgets.footer import Footer
# The window controls for pages without a menu bar - outlive every page too
from ..widgets.frame_widgets.window_chrome import CornerControls
# What Esc opens on a page with a menu bar
from ..widgets.frame_widgets.pause_menu import PauseMenu

# Dict mapping page names to page builder functions.
# Add new pages here to make them accessible by the router.
# All page builder functions should take a Context object as an argument and build the page as the root window's central widget.
PAGES: dict[str, type] = {
        "attacker": AttackerV0,
        "defender": DefenderV0,
        "demo/sprites": Sprites,
        "demo/boat_motion": BoatMotion,
        "demo/triangle": Triangle,
        "demo/visuals": Visuals,
        "demo/config_editor": ConfigEditor,
        "settings": SettingsPage,
        "theme_editor": ThemeEditorPage,
        "404": NotFound,
}

# Page builder classes for data-driven pages, keyed by the "build_type" a
# page's own config.json declares. PageManager discovers every config.json
# under assets/pages at startup; any key it finds with a build_type listed
# here gets merged into PAGES below so it navigates like any other page,
# without needing a hand-written entry above.
GENERIC_BUILD_TYPES: dict[str, type] = {
    "workspace": WorkspacePage,
    "title": TitlePage,
    "workspace_select": WorkspaceSelectPage,
}


# The app's entry point: assets/pages/start.json
START_PAGE = "start"
# Shown in place of any page that doesn't exist (see Router.show)
NOT_FOUND_PAGE = "404"


class Router:
    '''
    Handles page navigation by calling page builder functions. (Pages can't import each other because of circular imports)
    Builds the first page on startup (see start)
    '''
    
    def __init__(self, root: QMainWindow):
        '''
        Creates the app's Context object. The first page is built by
        start(), so App can decide when the window shows (see App).
        '''
        self.context: Context = Context(root, self)
        self.style = self.context.style
        self.navigation_stack: list[str] = []
        # Pages gone back from, most recent last - go_forward returns to them.
        # Going anywhere else clears it, as in a browser
        self.forward_stack: list[str] = []
        self.current_frame: QWidget | None = None
        self.current_page: str | None = None
        # The page key the 404 page reports as missing
        self.missing_page: str | None = None
        self.transition: PageTransition | None = None
        # Set once quitting, so a second quit (during FadeOut) doesn't start another
        self.quitting = False
        self.footer = Footer(root, self.context)
        self.corner_controls = CornerControls(self.context)
        self.pause_menu = PauseMenu(self.context)

        self.register_discovered_pages()

    def start(self, start_page: str | None = None):
        '''Builds the first page - START_PAGE if start_page isn't given. Called once by App.'''
        self.show(start_page or START_PAGE)

    def register_discovered_pages(self):
        '''
        Registers every data-driven page PageManager discovered whose
        build_type is known, without overriding a hand-written entry above,
        and drops any data-driven page that's no longer there. Called at
        startup, and again after pages are created or deleted while running
        (see the workspace editor).
        '''
        build_types = self.context.pages.build_types
        generic_classes = set(GENERIC_BUILD_TYPES.values())
        for key, page_class in list(PAGES.items()):
            if page_class in generic_classes and key not in build_types:
                del PAGES[key]
        for key, build_type in build_types.items():
            if key not in PAGES and build_type in GENERIC_BUILD_TYPES:
                PAGES[key] = GENERIC_BUILD_TYPES[build_type]

    def show(self, next_page: str, direction: int = 1, forward: bool = False):
        '''
        Displays the specified page, which should be a key in the PAGES dict. Clears the current page first.
        A key that isn't in PAGES (even START_PAGE, e.g. when assets/ is
        missing) shows the 404 page in its place. The missing key still goes
        on the navigation stack, so Back leaves the 404 page like any other.

        direction is which way the change animates (see PageTransition):
        1 going deeper, -1 going back, 0 a refresh of the same page.
        forward=True keeps the forward history (see go_forward) - any other
        new page clears it.

        Going to a page (direction 1) never piles up the history: the page
        you're already on does nothing, and a page already in the history
        goes back to it (see go_back_to) - Title from deep in a workspace
        returns to the start rather than stacking another start on top.
        '''
        # Handle first page ever (usually the start page or a reset)
        if len(self.navigation_stack) == 0:
            self.navigation_stack.append(next_page)
        elif direction == 1 and not forward:
            if next_page == self.navigation_stack[-1]:
                return  # already here
            if next_page in self.navigation_stack:
                self.go_back_to(next_page)
                return

        # Handle deeper page (not refresh) - leaving the current page the
        # same way go_back does, so it's autosaved, its processes stop, and
        # its animation/click callbacks don't outlive its widgets
        if not next_page == self.navigation_stack[-1]:
            self.context.reset_page()
            self.context.reset_build()
            self.context.start_build()
            self.context.start_page()
            self.navigation_stack.append(next_page)
            if not forward:
                self.forward_stack.clear()

        # Handle 404
        self.missing_page = next_page
        if next_page not in PAGES:
            print(f"Page '{next_page}' not found. Showing the 404 page.")
            next_page = NOT_FOUND_PAGE

        # Picture the page being left before it's torn down, for the transition
        # (skipped with transitions off - grabbing the page isn't free either)
        if self.transition is not None:
            self.transition.stop()
            self.transition = None
        performance = self.context.performance
        animate = performance.page_transitions
        snapshot = PageTransition.snapshot(self.context.root.centralWidget(), direction) if animate else None

        # Clear the window - and the pause menu, which was for the page being left
        self.pause_menu.close()
        self._clear_central_widget()

        # Call the page builder
        self.current_page = next_page
        started = performance.page_started()
        try:
            self.current_frame = PAGES[next_page](self.context)
            self.context.root.setCentralWidget(self.current_frame)
            performance.page_built(next_page, started)
            if animate:
                self.transition = PageTransition(self.current_frame, snapshot, direction)
        except Exception as e:
            self.context.reset_build()
            self._clear_central_widget()
            self.context.start_build()
            self.navigation_stack = []
            self.forward_stack.clear()
            if next_page == START_PAGE:
                # Nowhere left to fall back to - most likely broken assets
                print(f"Error building the start page: {e}. Showing the 404 page.")
                self.navigation_stack.append(START_PAGE)
                self.current_page = NOT_FOUND_PAGE
                self.current_frame = PAGES[NOT_FOUND_PAGE](self.context)
                self.context.root.setCentralWidget(self.current_frame)
            else:
                print(f"Error building page '{next_page}': {e}. Redirecting to the start page.")
                self.show(START_PAGE)

        # The new page's location, and any theme/zoom/label change it was rebuilt for
        self.footer.page_changed()
        self.corner_controls.page_changed()

    def _clear_central_widget(self):
        '''
        Detaches and schedules deletion of whatever the root window is
        currently showing, mirroring the old current_frame.destroy() call.
        '''
        old_frame = self.context.root.takeCentralWidget()
        if old_frame is not None:
            old_frame.deleteLater()

    def refresh(self, save: bool = True):
        '''
        Refreshes the current page by clearing the root window's central widget and rebuilding the current page.
        Useful for updating the UI after changing themes or making changes to the context.

        save=False skips autosaving the current page first - used when
        the caller has already reset or deleted this page's saved data
        (see ResetCurrentPageToDefaults) and wants the rebuild to pick up
        fresh config.json defaults instead of immediately re-saving
        whatever was still on screen.
        '''
        if save:
            self.context.save_page()
        self.context.reset_build()
        self.context.start_build()
        self.show(self.navigation_stack[-1], direction=0)

    def quit(self) -> bool:
        '''
        Deletes all ongoing processes and quits the app.
        Called on Close event (see MainWindow.closeEvent in app.py, wired
        up by KeyBinds) or by the Quit button. Returns whether the window
        should stay open for now - only while FadeOut plays, which quits
        once it's done.
        '''
        if self.quitting:
            return False  # already on the way out - quit() closing the window, say
        self.quitting = True
        self.context.reset_page()
        self.context.reset_build()
        # Stop the privileged helper last, so it restores any system state
        # and exits with the app rather than being orphaned.
        if hasattr(self.context, "helper"):
            self.context.helper.stop()
        root = self.context.root
        if self.context.preferences.is_fade_out() and root.isVisible() and not root.isMinimized():
            # Kept referenced - a window with no parent and no reference is deleted by Python mid-fade
            self.fade_out = FadeOut(root)
            self.fade_out.play(root, QApplication.instance().quit)
            return True
        QApplication.instance().quit()
        return False

    def go_back(self):
        '''
        Navigates backwards in the page history.
        '''
        if len(self.navigation_stack) < 2:
            return  # nowhere to go back to
        self.context.reset_page()
        self.context.reset_build()
        self.context.start_build()
        self.context.start_page()
        self.forward_stack.append(self.navigation_stack.pop())
        self.show(self.navigation_stack[-1], direction=-1)

    def go_back_to(self, key: str):
        '''
        Navigates back to the last time key is in the page history, as if
        Back were pressed until it showed - the pages gone back over are
        Forward's to return to, nearest first.
        '''
        stack = self.navigation_stack
        if key not in stack[:-1]:
            return
        index = len(stack) - 1 - stack[::-1].index(key)
        self.context.reset_page()
        self.context.reset_build()
        self.context.start_build()
        self.context.start_page()
        self.forward_stack.extend(reversed(stack[index + 1:]))
        del stack[index + 1:]
        self.show(key, direction=-1)

    def go_forward(self):
        '''
        Navigates forwards again, to the page last gone back from.
        '''
        if not self.forward_stack:
            return  # nowhere to go forward to
        self.show(self.forward_stack.pop(), forward=True)

    def page_name(self, key: str) -> str:
        '''A page's name as its links show it, or its own footer label, or just its key.'''
        config = self.context.pages.load_page_config(key)
        label_key = config.get("link_label") if isinstance(config.get("link_label"), str) else f"footer_pages_{key}"
        try:
            return self.context.labels.get(label_key)
        except KeyError:
            return key