from ...widgets.common import Common
from ...app_core.context import Context
from ...widgets.map import Map
from ...drawing.viewport import ViewPort


class AttackerV0:

    def __init__(self, context: Context):
        router, root = context.get_all()
        place = Common(context.ui_scale)

    # Menu bar
        menu = place.menu_bar(root, "Attacker Version 0")
        place.menu_bar_button(menu, "Quit", router.quit)
        place.menu_bar_button(menu, "Refresh", router.refresh)
        place.menu_bar_button(menu, "Toggle Theme", router.mode_toggle)
        place.menu_bar_button(menu, "Select Theme", router.select_theme)

    # Page sections

        left_p, middle_p, right_p = place.trifold(root)

    # NMap widget
        place.form_nmap(left_p)

    # ARP Spoofing widget
        place.form_arp_spoofing(left_p)

    # Sniffing widget
        place.form_sniff(left_p)

    # NFQ widget with modifiers
        place.form_mitm(left_p)
    # Dos widget
        place.form_dos(left_p)


    # Map
        map_frame = place.map_frame(middle_p)
        from ...drawing import sprites
        self.positions = sprites.random_spline_path(20, 100)
        self.color = "blue"
        world_map = Map(map_frame, self.draw_test_plane, 100)




    # Map
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
    

