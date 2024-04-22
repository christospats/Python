import tkinter as tk
from tkinter import ttk

#window
window = tk.Tk()
window.title('Frames and Parenting')
window.geometry('600x400')

#frame
frame = ttk.Frame(window, width=200, height=200, borderwidth=10, relief=tk.GROOVE)
frame.propagate(False)
frame.pack()

#master Setting
label = ttk.Label(frame,text='Label in Frame')
label.pack()

Button = ttk.Button(frame, text='button in Frame')
Button.pack()

#run
window.mainloop()