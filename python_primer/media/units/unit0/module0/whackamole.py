# whackamole with nerf gun

# Use programs written by others through "import"
import tkinter as tk  

# Define a window
window = tk.Tk()

# The instructions at the top
instructions = 'Click reset, then click fire to strike the mole'
label = tk.Label(text=instructions)
label.pack()

# Build a rectangular space on which to draw shapes like circles
w = 300
h = 200
canvas = tk.Canvas(master=window, width=w, height=h)
canvas.pack()

# These are variables that control the position of the target and nerf ball
targetX = 0
targetVX = 10
nerfX = 0
nerfY = h-10
nerfVX = 20
nerfVY = 0
nerfAY = -3
delT = 0.1
nerfFired = False


# This is what we want to do when the reset button is clicked:
def reset():
    global nerfFired, targetX, nerfX, nerfY, nerfVY
    nerfFired = False
    targetX = 0
    nerfX = 0
    nerfY = h-1
    nerfVY = 0
    canvas.delete("all")
    print('reset')

# When the fire button is clicked, we change the status of the nerf gun
def fire():
    # start launch
    global nerfFired
    nerfFired = True
    print('fired')

# Build the three buttons called "reset", "fire" and "quit"
frame = tk.Frame(master=window)
frame.pack()

resetb = tk.Button(
    master=frame, text="reset", relief=tk.RIDGE, fg='black', 
    bg='grey', height=2, width=5,command=reset)
resetb.grid(row=0, column=0)

fireb = tk.Button(
    master=frame, text="fire", relief=tk.RIDGE, fg='black', 
    bg='grey', height=2, width=5, command=fire)
fireb.grid(row=0, column=1)

quitb = tk.Button(
    master=frame, text="quit", relief=tk.RIDGE, fg='black', 
    bg='grey', height=2, width=5, command=window.destroy)
quitb.grid(row=0, column=2)

# This part of the code draws and animates
def run():
    global targetX, nerfX, nerfVY, nerfY
    canvas.delete("all")
    targetX += targetVX * delT
    canvas.create_rectangle(targetX, h-10, targetX+10, h, fill="green")
    if nerfFired:
        nerfX += nerfVX * delT
        nerfVY += nerfAY * delT
        nerfY += nerfVY * delT
    canvas.create_oval(nerfX+5,h-nerfY+5, nerfX+15, h-nerfY+15, fill="red")
    window.after(1, run)

# Launch the window and start the animation
window.after(1, run)
window.mainloop()

