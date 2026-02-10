from ...widgets.common import Common
from ...app_core.context import Context

class AttackerV0:

    def __init__(self, context: Context):
        router, root = context.get_all()
        place = Common(context.ui_scale)

        menu = place.menu_bar(root, "Attacker Version 0")
        place.menu_bar_button(menu, "Quit", router.quit)
        place.menu_bar_button(menu, "Refresh", router.refresh)
        place.menu_bar_button(menu, "Toggle Theme", router.mode_toggle)
        place.menu_bar_button(menu, "Select Theme", router.select_theme)
