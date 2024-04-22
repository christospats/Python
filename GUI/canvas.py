import tkinter as tk
from tkinter import ttk


def get_pos(event):
    print(f'x:{event.x} y:{event.y}')
    x = event.x
    y = event.y
    canvas.create_oval(x - 1, y - 1, x + 1, y + 1)


# window
window = tk.Tk()
window.title('canvas')
window.geometry('600x300')

# canvas
canvas = tk.Canvas(window, bg='white')
canvas.pack()

# canvas.create_rectangle((50, 20, 100, 200), fill='pink', width=0)
# canvas.create_line(0, 0, 100, 150)

canvas.bind('<B1-Motion>', get_pos)

# Button
clear = ttk.Button(window, text='Clear', command=lambda: canvas.delete('all'))
clear.pack()


# run
window.mainloop()
