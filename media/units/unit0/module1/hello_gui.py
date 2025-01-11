import tkinter as tk

window = tk.Tk()
canvas = tk.Canvas(master=window, width=500, height=400)
canvas.pack()

for i in range(1, 10):
    fontSize = i * 20
    fontStr = 'Times ' + str(fontSize) + ' italic bold'
    startx = 200 + 10 * i
    starty = 20 + i * 20
    canvas.create_text(
        startx, starty, text="Hello", font=fontStr, fill='grey')

window.mainloop()
