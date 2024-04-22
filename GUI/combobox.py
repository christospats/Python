import tkinter as tk
from tkinter import ttk

#window
window = tk.Tk()
window.title("Combobox and Spinbox")
window.geometry('600x600')

#combobox
items = ('Apex', 'League of Legends', 'Counter Strike')
games_string = tk.StringVar(value=items[0])
combobox = ttk.Combobox(window, textvariable=games_string)
combobox['values'] = items
#combobox.configure(values=items)
combobox.pack()

# events for combobox
combobox.bind('<<ComboboxSelected>>', lambda event: comboLabel.config(text=f'Selected Value: {games_string.get()}'))
comboLabel = ttk.Label(window,text='A Label')
comboLabel.pack()

#SpinBox
spin_int = tk.IntVar(value=12)
spinbox= ttk.Spinbox(window, from_=3, to=20, command=lambda: print(spin_int.get()), textvariable=spin_int)
spinbox.bind('<<Increment>>', lambda event: print('Up'))
spinbox.bind('<<Decrement>>', lambda event: print('Down'))
spinbox.pack()

#run
window.mainloop()