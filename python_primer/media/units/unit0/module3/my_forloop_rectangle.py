import tkinter as tk

window = tk.Tk()
canvas = tk.Canvas(master=window, width=200, height=100)
canvas.pack()

def draw_rectangles():
    for i in range(10, 51, 10):              
        canvas.create_rectangle(3*i, i, 3*i+20, i+10, outline="blue")

draw_rectangles()

window.mainloop()
