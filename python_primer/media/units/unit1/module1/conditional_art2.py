import random
from drawtool import DrawTool

dt = DrawTool()
dt.set_XY_range(0,10, 0,10)
dt.set_aspect('equal')

border = 1
x1 = random.uniform(0, 5)
y1 = 0
x2 = 10
y2 = random.uniform(0, 5)
colors = ['r','b','g','c','m','y','k']

n = 500
brush_size = 5
count = 0

structure = 0.9

for i in range(1000):

    # End the loop after n lines have been drawn:
    if count >= n:
        break

    # Pick a random coloe
    c = random.choice(colors)
    dt.set_color(c)

    # Draw a line from x1,y1 to x2,y2
    dt.draw_line(x1,y1, x2,y2)
    count += 1

    # The next start is the current end
    x1 = x2
    y1 = y2

    # Apply brush, depending on structure parameter
    increment = 1/brush_size
    if border == 1:                   # bottom
        x2 = 10
        y2 = random.uniform(0, 5)
        if random.random() < structure:
            for i in range(brush_size):
                x1 += increment
                y2 += increment
                dt.draw_line(x1,y1, x2,y2)
                count += 1
        border = 2
    elif border == 2:                  # right
        x2 = random.uniform(5, 10)
        y2 = 10
        if random.random() < structure:
            for i in range(brush_size):
                y1 += increment
                x2 -= increment
                dt.draw_line(x1,y1, x2,y2)
                count += 1
        border = 3
    elif border == 3:                  # top
        x2 = 0
        y2 = random.uniform(5, 10)
        if random.random() < structure:
            for i in range(brush_size):
                x1 -= increment
                y2 -= increment
                dt.draw_line(x1,y1, x2,y2)
                count += 1
        border = 4
    else:                              # left
        x2 = random.uniform(0, 5)
        y2 = 0
        if random.random() < structure:
            for i in range(brush_size):
                y1 -= increment
                x2 += increment
                dt.draw_line(x1,y1, x2,y2)
                count += 1
        border = 1

dt.display()
