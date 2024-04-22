import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.title('Tabs')
window.geometry('600x400')

# Notebook
notebook = ttk.Notebook(window)


tab1 = ttk.Frame(notebook)
label1 = ttk.Label(tab1, text='text in tab1')
label1.pack()
button1 = ttk.Button(tab1, text='Button in tab1')
button1.pack()

tab2 = ttk.Frame(notebook)
label2 = ttk.Label(tab2, text='text in tab2')
label2.pack()
button2 = ttk.Button(tab2, text='Button in tab1')
button2.pack()

notebook.add(tab1, text='Tab 1')
notebook.add(tab2, text='Tab 2')
notebook.pack()



#run
window.mainloop()