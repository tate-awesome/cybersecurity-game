from customtkinter import CTk, CTkFrame

from . import Context

# Import page builder objects here
# /demo
from ..pages.demo.sprites import Sprites
from ..pages.demo.boat_motion import BoatMotion
from ..pages.demo.triangle import Triangle

# /attacker
from ..pages.attacker.attacker import AttackerV0
from ..pages.defender.defender import DefenderV0

# /generic (data-driven pages, dispatched by each page's own config.json "build_type").
# title/start, title/select_mode, title/select_demo and title/select_lesson
# are all build_type "title" pages, discovered below - no hand-written
# entries needed for them.
from ..pages.generic import WorkspacePage, TitlePage

# Dict mapping page names to page builder functions.
# Add new pages here to make them accessible by the router.
# All page builder functions should take a Context object as an argument and build the page on the root CTk object.
PAGES: dict[str, type] = {
        "attacker/v0": AttackerV0,
        "defender/v0": DefenderV0,
        "demo/sprites": Sprites,
        "demo/boat_motion": BoatMotion,
        "demo/triangle": Triangle,
}

# Page builder classes for data-driven pages, keyed by the "build_type" a
# page's own config.json declares. PageManager discovers every config.json
# under assets/pages at startup; any key it finds with a build_type listed
# here gets merged into PAGES below so it navigates like any other page,
# without needing a hand-written entry above.
GENERIC_BUILD_TYPES: dict[str, type] = {
    "workspace": WorkspacePage,
    "title": TitlePage,
}


class Router:
    '''
    Handles page navigation by calling page builder functions. (Pages can't import each other because of circular imports)
    Builds the first page on startup
    '''
    
    def __init__(self, root: CTk, start_page: str | None = None):
        '''
        Creates the app's Context object and shows the first page.
        If start_page isn't given, it's read from the manifest's
        "startup_page" instead.
        '''
        self.context: Context = Context(root, self)
        self.style = self.context.style
        self.navigation_stack: list[str] = []
        self.current_frame: CTkFrame | None = None
        self.current_page: str | None = None

        # Register any data-driven page PageManager discovered whose
        # build_type is known, without overriding a hand-written entry above.
        for key, build_type in self.context.pages.build_types.items():
            if key not in PAGES and build_type in GENERIC_BUILD_TYPES:
                PAGES[key] = GENERIC_BUILD_TYPES[build_type]

        if start_page is None:
            start_page = self.context.pages.startup_page()
        self.show(start_page)

    def show(self, next_page: str):
        '''
        Displays the specified page, which should be a key in the PAGES dict. Clears the current page first.
        '''
        # Handle 404
        if next_page not in PAGES:
            print(f"Page '{next_page}' not found. Redirecting to title page.")
            self.navigation_stack = []
            next_page = "title/start"

        # Handle first page ever (usually title or 404 reset)
        if len(self.navigation_stack) == 0:
            self.navigation_stack.append(next_page)

        # Handle deeper page (not refresh)
        if not next_page == self.navigation_stack[-1]:
            self.navigation_stack.append(next_page)

        # Clear the window
        if self.current_frame is not None:
            self.current_frame.destroy()

        # Call the page builder
        self.current_page = next_page
        try:
            self.current_frame = PAGES[next_page](self.context)
        except Exception as e:
            print(f"Error building page '{next_page}': {e}. Redirecting to title page.")
            while len(self.context.root.winfo_children()) > 0:
                self.context.root.winfo_children()[0].destroy()

            self.navigation_stack = []
            self.current_page = "title/start"
            self.current_frame = PAGES["title/start"](self.context)

    def refresh(self):
        '''
        Refreshes the current page by clearing the root CTk object and rebuilding the current page.
        Useful for updating the UI after changing themes or making changes to the context.
        '''
        self.context.reset_build()
        self.context.start_build()
        self.show(self.navigation_stack[-1])

    def quit(self):
        '''
        Deletes all ongoing processes and destroys the CTk root.
        Called on Close event or by the Quit button.
        '''
        self.context.reset_build()
        self.context.reset_page()
        self.context.root.destroy()
    
    def go_back(self):
        '''
        Navigates backwards in the page history.
        '''
        if len(self.navigation_stack) < 1:
            return
        self.context.reset_build()
        self.context.reset_page()
        self.context.start_build()
        self.context.start_page()
        self.navigation_stack.pop()
        self.show(self.navigation_stack[-1])