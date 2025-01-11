import math
from drawtool import DrawTool

# Set up drawtool
dt = DrawTool()
dt.set_XY_range(-1,1, -1,1)
dt.set_aspect('equal')

def draw_circle_in_square(side):
    radius = side/2
    dt.set_color('r')
    dt.draw_circle(0,0, radius)
    return radius

def draw_square_in_circle(radius):
    side = math.sqrt(2) * radius
    dt.set_color('b')
    dt.draw_rectangle(-side/2, -side/2, side, side)
    return side

side = 1
dt.draw_rectangle(-side/2, -side/2, side, side)

n = 10
for i in range(n):
    radius = draw_circle_in_square(side)
    side = draw_square_in_circle(radius)

dt.display()
