import tkinter as tk
from tkinter import ttk

def button_func(entry_string):
    print(entry_string.get())

#window
window = tk.Tk()
window.title("Functions with arguments")

#widgets
entry_var = tk.StringVar(value='test')
entry = ttk.Entry(window, textvariable=entry_var)
entry.pack()


button = ttk.Button(window, text='Button', command=lambda: button_func(entry_var))
button.pack()

# run
window.mainloop()