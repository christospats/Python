import tkinter as tk
from tkinter import ttk

def button_func():
    entry_text = entry.get()
    label.config(text=entry_text)
    entry['state'] = 'disable'
def return_func():
    label.config(text='Testing')
    entry['state'] = 'active'
    
#window
window = tk.Tk()
window.title('Getting and setting widgets')

#widget
label = ttk.Label(master= window, text='Testing')
entry = ttk.Entry(master= window)
button = ttk.Button(master= window, text='My Button', command= button_func)
label.pack()
entry.pack()
button.pack()
return_button = ttk.Button(master=window, text='return', command= return_func)
return_button.pack()

#run
window.mainloop()
