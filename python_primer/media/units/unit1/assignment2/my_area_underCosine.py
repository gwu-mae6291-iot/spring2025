from drawtool import DrawTool
import random
import math

dt = DrawTool()
# Notice: x ranges between -1.57 and +1.57, y ranges between 0 and 1.
dt.set_XY_range(-1.57, 1.57, 0,1)
dt.set_aspect('equal')

random.seed(123)

# This draws the cosine function.
x = -1.57
m = 100
interval = (1.57-(-1.57))/m
dt.set_color('k')
for i in range(m):
    y = math.cos(x)
    dt.draw_point(x,y)
    x += interval


# Generate n=1000 random points.
n = 1000
# Count how many of them have their y value below sin(x)
count = 0

# Write your code here


print('area estimate =', (count/n)*3.141)
print('what theory predicts:', 2)

dt.display()