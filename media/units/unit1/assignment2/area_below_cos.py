from drawtool import DrawTool
import random
import math

dt = DrawTool()
# Notice: x ranges between -1.57 and 1.57 (where 1.57 approximates pi/2), y ranges between 0 and 1.
dt.set_XY_range(-1.57, 1.57, 0,1)
dt.set_aspect('equal')

# do not change this value: it makes 'random' numbers repeatable
random.seed(1012)

# This draws the cos function.
m = 100
x = -1.57
interval = 3.141/m
dt.set_color('k')
for i in range(m):
    y = math.cos(x)
    dt.draw_point(x,y)
    x += interval


# Generate n=1000 random points.
n = 1000
# Count how many of them have their y value below cos(x)
num_under = 0

# Write your code here



print('area estimate =', (num_under/n)*3.141)
print('what theory predicts:', 2)

dt.display()
