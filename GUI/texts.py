import tkinter as tk
from tkinter import ttk

def button_func():
    print('button was pressed')

def different_func():
    print('Hello')

#window
window = tk.Tk()
window.title('Window And Widgets')
window.geometry('800x500')

#ttk widgets
label = ttk.Label(master=window, text='This a Test')
label.pack()

#create widgets
text = tk.Text(master=window)
text.pack()

#ttk entry
entry = ttk.Entry(master=window)
entry.pack()

#new label and button
label_frame = ttk.Frame(master=window)
newLabel = ttk.Label(master=label_frame,text="my label")
newButton = ttk.Button(master=label_frame,text="Different button", command=different_func)
newLabel.pack(side='left', padx=10)
newButton.pack(side='left')
label_frame.pack(pady=10)


#ttk button
button = ttk.Button(master=window, text='Button', command=button_func)
button.pack()

#run
window.mainloop()