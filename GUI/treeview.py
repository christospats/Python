import tkinter as tk
from tkinter import ttk
from random import choice

# window
window = tk.Tk()
window.title('Treeview')
window.geometry('600x400')

# data
first_name = ['John', 'Bob', 'Anastasia', 'James']
last_name = ['Tr', 'Ross', 'something', 'Bond']

# treeview
treeview = ttk.Treeview(window, columns=('first', 'last', 'email'), show='headings')
treeview.heading('first', text='First Name')
treeview.heading('last', text='Last Name')
treeview.heading('email', text='Email')
# treeview.insert(parent='', index=0, values=('John', 'Doe', 'John@gmail.com'))
for i in range(50):
    first = choice(first_name)
    last = choice(last_name)
    email = f'{first}{last}@gmail.com'
    data = (first, last, email)
    treeview.insert(parent='', index=tk.END, values=data)


def item_select(_):
    for i in treeview.selection():
        print(treeview.item(i)['values'])


def delete_items(_):
    for i in treeview.selection():
        treeview.delete(i)


treeview.bind('<<TreeviewSelect>>', item_select)

treeview.bind('<Delete>', delete_items)


treeview.pack(fill='both', expand=True)

# run
window.mainloop()