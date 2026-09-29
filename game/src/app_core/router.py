from PySide6.QtWidgets import QApplication, QMainWindow, QWidget

from . import Context

# Import page builder objects here
# /demo
from ..pages.demo.sprites import Sprites
from ..pages.demo.boat_motion import BoatMotion
from ..pages.demo.triangle import Triangle
from ..pages.demo.visuals import Visuals

# /attacker
from ..pages.attacker.attacker import AttackerV0
from ..pages.defender.defender import DefenderV0

# /generic (data-driven pages, dispatched by each page's own config "build_type").
# start, title/select_mode and title/select_demo are build_type "title" pages
# and title/select_lesson is "lesson_select", all discovered below - no
# hand-written entries needed for them.
from ..pages.generic import WorkspacePage, TitlePage, LessonSelectPage

# Hard-coded 404 page - needs nothing from assets/, so it still works without it
from ..pages.not_found import NotFound

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
    "lesson_select": LessonSelectPage,
}


# The app's entry point: assets/pages/start.json
START_PAGE = "start"
# Shown in place of any page that doesn't exist (see Router.show)
NOT_FOUND_PAGE = "404"


class Router:
    '''
    Handles page navigation by calling page builder functions. (Pages can't import each other because of circular imports)
    Builds the first page on startup
    '''
    
    def __init__(self, root: QMainWindow, start_page: str | None = None):
        '''
        Creates the app's Context object and shows the first page.
        If start_page isn't given, it's START_PAGE.
        '''
        self.context: Context = Context(root, self)
        self.style = self.context.style
        self.navigation_stack: list[str] = []
        self.current_frame: QWidget | None = None
        self.current_page: str | None = None
        # The page key the 404 page reports as missing
        self.missing_page: str | None = None

        # Register any data-driven page PageManager discovered whose
        # build_type is known, without overriding a hand-written entry above.
        for key, build_type in self.context.pages.build_types.items():
            if key not in PAGES and build_type in GENERIC_BUILD_TYPES:
                PAGES[key] = GENERIC_BUILD_TYPES[build_type]

        if start_page is None:
            start_page = START_PAGE
        self.show(start_page)

    def show(self, next_page: str):
        '''
        Displays the specified page, which should be a key in the PAGES dict. Clears the current page first.
        A key that isn't in PAGES (even START_PAGE, e.g. when assets/ is
        missing) shows the 404 page in its place. The missing key still goes
        on the navigation stack, so Back leaves the 404 page like any other.
        '''
        # Handle first page ever (usually the start page or a reset)
        if len(self.navigation_stack) == 0:
            self.navigation_stack.append(next_page)

        # Handle deeper page (not refresh)
        if not next_page == self.navigation_stack[-1]:
            self.navigation_stack.append(next_page)

        # Handle 404
        self.missing_page = next_page
        if next_page not in PAGES:
            print(f"Page '{next_page}' not found. Showing the 404 page.")
            next_page = NOT_FOUND_PAGE

        # Clear the window
        self._clear_central_widget()

        # Call the page builder
        self.current_page = next_page
        try:
            self.current_frame = PAGES[next_page](self.context)
            self.context.root.setCentralWidget(self.current_frame)
        except Exception as e:
            self.context.reset_build()
            self._clear_central_widget()
            self.context.start_build()
            self.navigation_stack = []
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
        (see ContextManager.reset_data) and wants the rebuild to pick up
        fresh config.json defaults instead of immediately re-saving
        whatever was still on screen.
        '''
        if save:
            self.context.save_page()
        self.context.reset_build()
        self.context.start_build()
        self.show(self.navigation_stack[-1])

    def quit(self):
        '''
        Deletes all ongoing processes and quits the app.
        Called on Close event (see MainWindow.closeEvent in app.py, wired
        up by KeyBinds) or by the Quit button.
        '''
        self.context.reset_page()
        self.context.reset_build()
        QApplication.instance().quit()

    def go_back(self):
        '''
        Navigates backwards in the page history.
        '''
        if len(self.navigation_stack) < 1:
            return
        self.context.reset_page()
        self.context.reset_build()
        self.context.start_build()
        self.context.start_page()
        self.navigation_stack.pop()
        self.show(self.navigation_stack[-1])