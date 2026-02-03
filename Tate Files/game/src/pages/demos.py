from ..widgets.common import Common as place
from ..widgets.map import Map as map

class Demos:

    def map(root):
        menu_bar = place.menu_bar(root, "Demo")
        place.menu_bar_button(menu_bar, "Button1", None)
        place.trifold(root)
        return