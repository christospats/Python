import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.geometry('600x400')
window.title('Menu')

#Menu

menu = tk.Menu(window)

#sub Menu
file_menu= tk.Menu(menu, tearoff=False)
file_menu.add_command(label='New', command=lambda : print('New File'))
file_menu.add_command(label='Open', command=lambda : print('Open File'))
file_menu.add_separator()
menu.add_cascade(label='File', menu=file_menu)

# Sub menu2
help_menu = tk.Menu(menu, tearoff=False)
help_menu.add_command(label='Help entry', command=lambda : print(help_check.get()))

help_check = tk.StringVar()
help_menu.add_checkbutton(label='check', onvalue='on', offvalue='off',variable=help_check)

menu.add_cascade(label='Help', menu=help_menu)

exercise_menu = tk.Menu(menu, tearoff=False)
exercise_menu.add_command(label='exercise command 1')
menu.add_cascade(label='Excercise', menu=exercise_menu)

ex_sub_menu = tk.Menu(menu, tearoff=False)
ex_sub_menu.add_command(label='Some More Stuff')
exercise_menu.add_cascade(label='More Stuff', menu=ex_sub_menu)

window.configure(menu=menu)

# Menu button
menu_button = ttk.Menubutton(window, text="Menu Button")
menu_button.pack()

menu_sub_button = tk.Menu(menu_button, tearoff=False)
menu_sub_button.add_command(label='Entry 1', command=lambda : print('test 1'))
menu_sub_button.add_checkbutton(label='Check 1')
menu_button.configure(menu=menu_sub_button)


#run
window.mainloop()