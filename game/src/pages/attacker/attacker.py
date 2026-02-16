from ...app_core.context import Context

from ...widgets.style import Style
from ...widgets import common, forms, popup
from ...widgets.map import Map
from ...drawing.viewport import ViewPort


class AttackerV0:

    def __init__(self, context: Context):
        router = context.router
        root = context.root
        style = Style(context.ui_scale)

    # Menu bar
        menu = common.menu_bar(style, root, "Attacker Version 0")
        common.menu_bar_button(style, menu, "Quit", router.quit)
        common.menu_bar_button(style, menu, "Refresh", router.refresh)
        common.menu_bar_button(style, menu, "Toggle Theme", router.mode_toggle)
        common.menu_bar_button(style, menu, "Select Theme", router.select_theme)
        common.menu_bar_button(style, menu, "Help", lambda:popup.open(style,root,context.help_message()))

    # Page sections

        left_p, middle_p, right_p = common.trifold(style, root)

    # NMap widget
        forms.nmap(style, left_p)

    # ARP Spoofing widget
        forms.arp(style, left_p)

    # Sniffing widget
        forms.sniff(style, left_p)

    # NFQ widget with modifiers
        forms.mitm(style, left_p)
    # Dos widget
        forms.dos(style, left_p)


    # Map
        from ...drawing import sprites
        self.positions = sprites.random_spline_path(20, 100)
        self.color = "blue"
        world_map = Map(style, right_p, self.draw_test_plane, 100)




    # Map callback
    def draw_test_plane(self, canvas, draw_lock, scale: float, offset: tuple[float, float]):
        import time
        from ...drawing import transformations as t

        path_duration = 30.0
        path_index = int(((time.time() % path_duration) / path_duration) * (len(self.positions)-2))
        bearing = t.get_bearing(self.positions[path_index], self.positions[path_index+1])
        draw = ViewPort(canvas, scale, offset)
        with draw_lock:
            canvas.delete("all")
            draw.bbox()
            draw.grid_lines()
            draw.line(self.positions, self.color)
            last_position = self.positions[path_index]
            draw.boat(last_position, bearing)
    

