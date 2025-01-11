import tkinter as tk
import time

window = tk.Tk()
canvas = tk.Canvas(master=window, width=200, height=100)
canvas.pack()

i = 10

def draw_rectangles():
    global i
    canvas.delete('all')
    canvas.create_rectangle(3*i, i, 3*i+20, i+10, outline="blue")
    if i < 51:
        i = i + 1
        time.sleep(0.25)
        window.after(1, draw_rectangles)

window.after(1, draw_rectangles)
window.mainloop()
