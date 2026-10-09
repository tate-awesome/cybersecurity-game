from ...app_core import Context
from ...pages.page import Page
from ...widgets import MenuBar, VISUALS, VisualBackground
from ...widgets.frame_widgets.menu_bar import DEMO_MENU_BAR


class Visuals(Page):
    '''
    Demo page for the procedural visuals (see widgets/visuals). A menu bar
    dropdown picks which one plays; "Background Preview" blurs it the way
    the title pages do, to judge how it reads behind text; "Detailed"
    switches between the detailed and simple versions; "Replay Startup"
    plays its startup animation again.
    The theme buttons are here to check each visual in every palette.
    '''

    # Match the "blur" in the title pages' "background" configs
    BACKGROUND_BLUR = 6.0

    # Kept on the class so they survive the page rebuild that the theme
    # buttons trigger (see Style.toggle_mode/select_theme -> router.refresh)
    selected_key: str | None = None
    preview: bool = False
    detailed: bool = True

    def __init__(self, context: Context):
        super().__init__(context)
        labels = context.labels

        menu_bar = MenuBar(self, context, "visuals_demo")

        # Display name -> visual key, in registry order, plus the cycle option
        keys = [*VISUALS, "cycle"]
        names = {labels.get(f"visual_names_{key}"): key for key in keys}
        if Visuals.selected_key not in keys:
            Visuals.selected_key = keys[0]

        self.background = VisualBackground(
            self, context, Visuals.selected_key,
            blur=self.BACKGROUND_BLUR if Visuals.preview else 0.0,
            paint_options={"packets": Visuals.detailed},
        )

        menu_bar.add_dropdown(
            list(names),
            self.select,
            default=labels.get(f"visual_names_{Visuals.selected_key}"),
        )
        self.names = names
        menu_bar.add_checkbox(labels.get("menu_bar_buttons_background_preview"), Visuals.preview, self.set_preview)
        menu_bar.add_checkbox(labels.get("menu_bar_buttons_visual_detailed"), Visuals.detailed, self.set_detailed)
        menu_bar.add_button("replay_intro", self.background.replay_intro)
        menu_bar.add_config_buttons(DEMO_MENU_BAR)

    def select(self, name: str):
        Visuals.selected_key = self.names[name]
        self.background.set_visual(Visuals.selected_key)

    def set_detailed(self, on: bool):
        '''Detailed (as on title pages) or simple (as in workspaces, by default) - see Visual.detailed.'''
        Visuals.detailed = on
        self.background.paint_options = {**self.background.paint_options, "packets": on}
        self.background.invalidate()

    def set_preview(self, on: bool):
        Visuals.preview = on
        self.background.set_blur(self.BACKGROUND_BLUR if on else 0.0)
