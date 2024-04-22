import tkinter as tk
from tkinter import ttk

#window
window = tk.Tk()
window.title('Buttons')
window.geometry('600x400')

#Buttons
def button_func():
    print('A basic Button')
    print(radio_var.get())

button_sting = tk.StringVar(value='A Simple Button')
button = ttk.Button(window, text='A Simple Text',command=button_func,textvariable=button_sting)
button.pack()

#Checkbox
check_var = tk.IntVar()
check = ttk.Checkbutton(window, text='Checkbox 1', command=lambda: print(check_var.get()), variable=check_var, onvalue=10, offvalue=5)
check.pack()

check2 = ttk.Checkbutton(window, text='CheckBox 2', command=lambda: print(check_var.set(5)))
check2.pack()

#radio buttons
radio_var = tk.StringVar()
radio1 = ttk.Radiobutton(window, text='RadioButton1', variable=radio_var, command=lambda: print(radio_var.get()))
radio1.pack()

radio2 = ttk.Radiobutton(window, text='RadioButton2', value=2,variable=radio_var)
radio2.pack()

#Ex
def exercise_func():
    print(check_bool.get())
    check_bool.set(False)


exercise_var = tk.StringVar()
check_bool = tk.BooleanVar()

exercise_radio1= ttk.Radiobutton(window, text='Radio1', value='A', command=exercise_func, variable=exercise_var)
exercise_radio2= ttk.Radiobutton(window, text='Radio2', value='B', command=exercise_func, variable=exercise_var)


exercise_check= ttk.Checkbutton(window, text='Checkbutton', variable=check_bool, command= lambda: print(exercise_var.get()))
exercise_radio1.pack()
exercise_radio2.pack()
exercise_check.pack()
#run
window.mainloop()