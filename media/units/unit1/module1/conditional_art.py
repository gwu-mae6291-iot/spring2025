import random
from drawtool import DrawTool

# Set up drawtool
dt = DrawTool()
dt.set_XY_range(0,10, 0,10)
dt.set_aspect('equal')

# To start, pick one endpoint on bottom border
x1 = random.uniform(0,10)
y1 = 0
# And the other on the right side
x2 = 10
y2 = random.uniform(0,10)

colors = ['r','b','g','c','m','y','k']
n = 100

for i in range(n):
    # Pick a random color
    c = random.choice(colors)
    dt.set_color(c)

    # Draw a line from x1,y1 to x2,y2
    dt.draw_line(x1,y1, x2,y2)

    # The next start is the current end
    x1 = x2
    y1 = y2

    # Change x2,y2 by picking a random border:
    border = random.choice([1,2,3,4])

    # Then pick a random point on the chosen border
    if border == 1:
        x2 = random.uniform(0,10)
        y2 = 0
    elif border == 2:
        x2 = 10
        y2 = random.uniform(0,10)
    elif border == 3:
        x2 = random.uniform(0,10)
        y2 = 10
    else:
        x2 = 0
        y2 = random.uniform(0,10)

dt.display()
