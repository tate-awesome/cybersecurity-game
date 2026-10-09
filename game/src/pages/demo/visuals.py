from ...app_core import Context
from ...pages.page import Page
from ...widgets import MenuBar, VISUALS, VisualBackground
from ...widgets.frame_widgets.menu_bar import DEMO_MENU_BAR


class Visuals(Page):
    '''
    Demo page for the procedural visuals (see widgets/visuals). A menu bar
    dropdown picks which one plays - and makes it the app's background, the
    same preference as the settings page's Background Type (so it opens on
    whichever that is); "Background Preview" blurs it the way
    the title pages do, to judge how it reads behind text; "Detailed"
    switches between the detailed and simple versions; "Replay Startup"
    plays its startup animation again.
    The theme buttons are here to check each visual in every palette.
    '''

    # Match the "blur" in the title pages' "background" configs
    BACKGROUND_BLUR = 6.0

    # Kept on the class so they survive the page rebuild that the theme
    # buttons trigger (see Style.toggle_mode/set_theme -> router.refresh).
    # The visual itself is the background preference, Style.background_visual.
    preview: bool = False
    detailed: bool = True

    def __init__(self, context: Context):
        super().__init__(context)
        labels = context.labels

        menu_bar = MenuBar(self, context, "visuals_demo")

        # Display name -> visual key, in registry order, plus the cycle option
        keys = [*VISUALS, "cycle"]
        names = {labels.get(f"visual_names_{key}"): key for key in keys}
        selected = self.style.background_visual if self.style.background_visual in keys else keys[0]

        self.background = VisualBackground(
            self, context, selected,
            blur=self.BACKGROUND_BLUR if Visuals.preview else 0.0,
            paint_options={"packets": Visuals.detailed},
        )

        menu_bar.add_dropdown(
            list(names),
            self.select,
            default=labels.get(f"visual_names_{selected}"),
        )
        self.names = names
        menu_bar.add_checkbox(labels.get("menu_bar_buttons_background_preview"), Visuals.preview, self.set_preview)
        menu_bar.add_checkbox(labels.get("menu_bar_buttons_visual_detailed"), Visuals.detailed, self.set_detailed)
        menu_bar.add_button("replay_intro", self.background.replay_intro)
        menu_bar.add_config_buttons(DEMO_MENU_BAR)

    def select(self, name: str):
        key = self.names[name]
        self.background.set_visual(key)
        # Also the app's background from now on (saved, like the settings page's Background Type)
        self.style.set_background(visual=key)

    def set_detailed(self, on: bool):
        '''Detailed (as on title pages) or simple (as in workspaces, by default) - see Visual.detailed.'''
        Visuals.detailed = on
        self.background.paint_options = {**self.background.paint_options, "packets": on}
        self.background.invalidate()

    def set_preview(self, on: bool):
        Visuals.preview = on
        self.background.set_blur(self.BACKGROUND_BLUR if on else 0.0)
