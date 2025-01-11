# Abandoned becaus
from drawtool import DrawTool
import random
import math

dt = DrawTool()
dt.set_XY_range(0,6.28, -1,1)
dt.set_aspect('auto')

# First, a yellow background of random circles
dt.set_color('y')
for i in range(100):
    x = 6.28 * random.random()
    y = 2 * random.random() - 1
    dt.draw_point(x, y)

# Now, different color circles along the function
colors = ['r','b','g','m','k','c']

n = 100
x_spacing = 6.28/n

x = 0
for i in range(n):
    f = math.sin(x)
    r = 0.25 * random.random()   # random radius
    c = random.choice(colors)    # random color
    dt.set_color(c)
    dt.draw_circle(x, f, 0.1)
    x = x + x_spacing

dt.display()
