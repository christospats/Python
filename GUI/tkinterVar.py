import tkinter
import tkinter as tk
from tkinter import ttk

def button_func():
    print(string_variables.get())
    string_variables.set('Button Pressed')

#window
window = tk.Tk()
window.title('Tkinter Variables')
window.geometry('300x100')

#Tk variables
string_variables = tk.StringVar()

#widgets
label = ttk.Label(master=window, text='label', textvariable=string_variables)
label.pack()
entry = ttk.Entry(master=window, textvariable=string_variables)
entry.pack()
button = ttk.Button(master=window, text='My button', command=button_func)
button.pack()
#run
window.mainloop()