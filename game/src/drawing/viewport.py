from . import transformations as t
from customtkinter import CTkCanvas
from math import pi as PI
import time

class ViewPort:
    '''
    Holds the current viewport parameters for drawing on the canvas for a single frame.
    '''
    def __init__(self, canvas: CTkCanvas, scale: float, offset: tuple[float, float], padding=20, input_range=((0,0),(200,200))):
        self.canvas = canvas
        self.scale = scale
        self.offset = offset
        self.padding = padding
        self.input_range = input_range

    def background(self, color: str):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        self.canvas.create_rectangle(0, 0, w, h, fill=color)

    def ocean(self):
        self.background("#003459")
    
    def bbox(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        o = 3
        self.canvas.create_rectangle(0,0,w-o/2,h-o/2,fill="",outline="black", width=o)

    def test_triangle(self):
        '''
        Visualize the transformations
        '''

        # Gridlines
        for i in range(-5, 6):
            h_line = [ (-1, i), (1, i) ]
            h_line = t.scale(h_line, 5)

            v_line = t.rotate(h_line, PI/2, (0, 0))

            h_line = t.padded_fit_uniform(h_line, (-5, -5), (5, 5), self.canvas, self.padding)
            v_line = t.padded_fit_uniform(v_line, (-5, -5), (5, 5), self.canvas, self.padding)

            h_line = t.zoom_and_pan(h_line, self.scale, self.offset)
            v_line = t.zoom_and_pan(v_line, self.scale, self.offset)
            color = "black"
            if i == 0:
                color = "red"

            self.canvas.create_line(t.flatten(h_line), width=2, fill=color)
            self.canvas.create_line(t.flatten(v_line), width=2, fill=color)

        # Triangle
        triangle = [ (-1,0), (0,2), (1,0) ]          #   /.\  centered on a 10x10 plane with origin at 0
        triangle = t.scale(triangle, 2.0, (0,0))
        angle = (time.time() % 20.0) * PI / 10.0
        triangle = t.rotate(triangle, angle, (0,0))  #   <.   
        triangle = t.padded_fit_uniform(triangle, (-5, -5), (5, 5), self.canvas, self.padding)
        triangle = t.zoom_and_pan(triangle, self.scale, self.offset)
        self.canvas.create_polygon(triangle, fill="green", width="5", outline="blue")

        # Inscribed circle
        circle_box = [ (-2,-2), (2,2) ]
        circle_box = t.scale(circle_box, 2.0, (0,0)) 
        circle_box = t.padded_fit_uniform(circle_box, (-5, -5), (5, 5), self.canvas, self.padding)
        circle_box = t.zoom_and_pan(circle_box, self.scale, self.offset)
        self.canvas.create_oval(circle_box, fill="", outline="blue", width="3")


    def line(self, points: list[tuple[float, float]], line_color: str):
        '''
        Draws the path of the points 
        '''
        if len(points) < 2:
            return
        points = t.padded_fit_uniform(points, self.input_range[0], self.input_range[1], self.canvas, self.padding)
        points = t.zoom_and_pan(points, self.scale, self.offset)
        self.canvas.create_line(points, width=2, fill=line_color)


    def grid_lines(self):
        for i in range(0, 210, 10):
            h_line = [ (0, i), (200, i) ]

            v_line = t.rotate(h_line, PI/2, (i, i))

            h_line = t.padded_fit_uniform(h_line, self.input_range[0], self.input_range[1], self.canvas, self.padding)
            v_line = t.padded_fit_uniform(v_line, self.input_range[0], self.input_range[1], self.canvas, self.padding)

            h_line = t.zoom_and_pan(h_line, self.scale, self.offset)
            v_line = t.zoom_and_pan(v_line, self.scale, self.offset)
            color = "black"
            if i == 0:
                color = "red"

            self.canvas.create_line(t.flatten(h_line), width=2, fill=color)
            self.canvas.create_line(t.flatten(v_line), width=2, fill=color)


    def boat(self, position: tuple[float, float], bearing: float, fill_color="gray", line_color="black"):
        the_boat = [
                            (-2, 1),
                            (-2, -1),
                            (1,  -1),
                            (3,  0),
                            (1,  1)
                        ]
        the_boat = t.rotate(the_boat, bearing)
        the_boat = t.scale(the_boat, 2)

        the_boat = t.translate(the_boat, position)
        
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
    
        the_boat = t.padded_fit_uniform(the_boat, self.input_range[0], self.input_range[1], self.canvas, 20)
        the_boat = t.zoom_and_pan(the_boat, self.scale, self.offset)
        self.canvas.create_polygon(the_boat, fill=fill_color, outline=line_color)