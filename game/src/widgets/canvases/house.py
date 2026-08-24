from .core.canvas import Canvas
from ...app_core import Context
from customtkinter import CTkFrame

class House(Canvas):
    def __init__(self, master: CTkFrame, context: Context):
        super().__init__(master, context, ((0, 0), (100, 100)))
        self.buffer = context.net.buffer.hvac

        def frame_callback():
            def color(key):
                return self.context.style.color(self.context.states.get("hvac_house_colors", key))
            def sprite(key):
                return self.context.states.get("hvac_house_sprites", key)
            def sprite_enabled(key):
                # A malformed/non-numeric sprite config value would otherwise
                # raise on every frame, permanently freezing this canvas.
                try:
                    return int(sprite(key)) == 1
                except (TypeError, ValueError):
                    return False

            self.delete("all")

            if sprite_enabled("background"):
                self.draw.background(color("background"))

            if self.winfo_width() <= 1 or self.winfo_height() <= 1:
                return

            # The house (slave) sends its temperature to the controller (master); the controller
            # sends the heater command back. "in" is what this MITM vantage point received (the
            # sender's true value), "out" is what it forwarded on (possibly altered in transit).
            temperature_sent_by_house = self.buffer.get_temperature("in")       # house -> controller
            temperature_seen_by_controller = self.buffer.get_temperature("out") # house -> controller
            heater_commanded_by_controller = self.buffer.get_heater("in") == 1  # controller -> house
            heater_seen_by_house = self.buffer.get_heater("out") == 1           # controller -> house

            fill = color("fill")
            outline = color("line_art")
            text = color("text")
            coldness = color("coldness")
            hotness = color("hotness")

            # Lay the controller above the room on a tall/square canvas, or to its left on a wide
            # canvas, so the vent wall it drives always sits nearest to it.
            if self.winfo_width() > self.winfo_height():
                controller_bl, controller_tr = (4, 25), (30, 75)
                room_bl, room_tr = (30, 8), (94, 92)
                vent_wall, back_wall = "left", "right"
            else:
                controller_bl, controller_tr = (25, 70), (75, 96)
                room_bl, room_tr = (8, 6), (92, 70)
                vent_wall, back_wall = "top", "bottom"

            # Room: back wall carries the thermostat and a leaky window, the wall facing the
            # controller carries the heater vent it actuates.
            if sprite_enabled("room"):
                self.draw.hvac_room(room_bl, room_tr, fill, outline)

            if sprite_enabled("room_thermostat"):
                thermostat_position = ((room_bl[0] + room_tr[0]) / 2, (room_bl[1] + room_tr[1]) / 2)
                self.draw.hvac_thermostat(thermostat_position, temperature_sent_by_house, fill, outline, text)

            if sprite_enabled("window"):
                self.draw.hvac_window(room_bl, room_tr, back_wall, 0.72, outline, coldness)
                self.draw.hvac_flow_arrows(room_bl, room_tr, back_wall, 0.72, coldness)

            if sprite_enabled("vent"):
                vent_fill = hotness if heater_seen_by_house else ""
                self.draw.hvac_vent(room_bl, room_tr, vent_wall, 0.5, outline, vent_fill)
                if heater_seen_by_house:
                    self.draw.hvac_flow_arrows(room_bl, room_tr, vent_wall, 0.5, hotness)

            # Controller: its own thermostat shows the temperature it is acting on, and the
            # indicator shows the heater command it is issuing - red/OPEN when calling for heat
            # (too cold), blue/CLOSED when satisfied (too hot).
            if sprite_enabled("controller_box"):
                self.draw.hvac_controller_box(controller_bl, controller_tr, fill, outline)

            # The thermostat's status label needs room both above and below its dial, while the
            # indicator only needs room below - so they're spaced unevenly to avoid colliding.
            box_w = controller_tr[0] - controller_bl[0]
            box_h = controller_tr[1] - controller_bl[1]
            if box_w >= box_h:
                y = controller_bl[1] + box_h * 0.42
                thermostat_center = (controller_bl[0] + box_w * 0.26, y)
                indicator_center = (controller_bl[0] + box_w * 0.74, y)
            else:
                x = controller_bl[0] + box_w * 0.5
                thermostat_center = (x, controller_bl[1] + box_h * 0.26)
                indicator_center = (x, controller_bl[1] + box_h * 0.80)

            if sprite_enabled("controller_thermostat"):
                if heater_commanded_by_controller:
                    status, status_color = "too cold!", coldness
                else:
                    status, status_color = "too hot!", hotness
                self.draw.hvac_thermostat(thermostat_center, temperature_seen_by_controller, fill, outline, text,
                                           status=status, status_color=status_color)

            if sprite_enabled("indicator"):
                self.draw.hvac_indicator(indicator_center, heater_commanded_by_controller, hotness, coldness, text)

        self.set_frame_callback(frame_callback)
        self.start_animation()
