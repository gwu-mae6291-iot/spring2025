import random
from drawtool import DrawTool

dt = DrawTool()
dt.set_XY_range(-10,10, -10,10)
dt.set_aspect('equal')

step = 0.5

def do_walk(x, y):
    num_steps = 0
    while True:
        direction = random.choice(['N','S','W','E'])
        if direction == 'N':
            y += step
        elif direction == 'S':
            y -= step
        elif direction == 'E':
            x += step
        else:
            x -= step
        if (x >= 10) or (x <= -10) or (y >= 10) or (y <= -10):
            break
        dt.draw_point(x, y)
        num_steps += 1
    return num_steps

num_walks = 10
for i in range(num_walks):
    # Pick a random color
    colors = ['r','b','g','c','m','y','k']
    c = random.choice(colors)
    dt.set_color(c)
    # Pick a random starting point
    x = random.uniform(-10, 10)
    y = random.uniform(-10, 10)
    n = do_walk(x, y)
    print(n)

dt.display()
