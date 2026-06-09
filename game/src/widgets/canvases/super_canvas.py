'''
Notes
'''

# --------------------------------------------------------------------------------------------------------------------------
#                                                     FRAME CALLBACKS
# --------------------------------------------------------------------------------------------------------------------------



def draw_boat_display(self, canvas, draw_lock, scale: float, offset: tuple[float, float]):
        bearing = self.buffer.get_bearing("in")
        draw = ViewPort(canvas, 1.0, (0,0), 20, ((-100, -100), (100, 100)))
        rudder = self.buffer.get_rudder("in")
        speed = self.buffer.get_speed("in")
        size = 33.3333
        with draw_lock:
            canvas.delete("all")
            draw.test_triangle()
            # draw.ocean()
            draw.boat((0,0), bearing+math.pi, "blue", "blue", scale=size*speed/5)
            draw.boat((0,0), 0, "grey", "black", scale=size)
            draw.arc((0, 0), 90, bearing, rudder+bearing, "red")
            draw.line([(0,0), (-speed*math.cos(bearing)*50, -speed*math.sin(bearing)*50)], "blue")

def sprite_test(self, canvas: CTkCanvas, draw_lock: Lock, scale: float, offset: tuple[float, float]):
    draw = ViewPort(canvas, scale, offset)
    with draw_lock:
        canvas.delete("all")
        draw.ocean()
        draw.line([(0, 0), (200, 200)], "white")
        draw.boat((100,100), 0)
        draw.boat((100,100), 3.14/2)
        draw.boat((100,100), -3.14/4)
        draw.boat((0,0), -3.14/4)
        draw.boat((200,0), -3.14/4)
        draw.boat((0,200), -3.14/4)
        draw.boat((200,200), -3.14/4)

def draw_defender_map(canvas, draw_lock, scale, offset):
        draw = ViewPort(canvas, scale, offset)
        with draw_lock:
            self._map_scale  = scale
            self._map_offset = offset
            canvas.delete("all")
            draw.grid_lines()
            if len(self._positions) < 1:
                return
            draw.line(self._positions, "red")
            if self._last_bearing is None:
                return
            draw.boat(self._positions[-1], self._last_bearing, "white", "black")

# --------------------------------------------------------------------------------------------------------------------------
#                                                     DRAWING FUNCTIONS
# --------------------------------------------------------------------------------------------------------------------------

