import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from secondScreen import secondScreen

filepaths = []

def checklist(continueButton, files):
    if not files.get_children():
        continueButton.config(state='disable')
    else:
        continueButton.config(state='normal')


# Button Functions
def importfunc():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        filepaths.append(file_path)
        # Extract filename without extension
        filename = os.path.splitext(os.path.basename(file_path))[0]
        print("Uploaded file:", filename)
        files.insert(parent='', index=tk.END, values=(filename,))
    checklist(continueButton, files)
    print(filepaths)


# Treeview Binds
def item_delete(_):
    for i in files.selection():
        files.delete(i)
    checklist(continueButton,files)


def continuefunc():
    secondScreen(files, filepaths)

# window
window = tk.Tk()
window.minsize(600,400)
window.title('Technical Analysis')
window.iconbitmap('moneyincrease_118078.ico')

# widgets
instructions = ttk.Label(window,
                         text='Choose import and select the files you want. When you are ready press continue. If you want to delete a file, choose it and press delete',
                         wraplength=600)
instructions.pack()

# treeview
files = ttk.Treeview(window, columns=('Name'), show='headings')
files.heading('Name', text='File Name')
files.pack(fill='both', expand=True)

files.bind('<Delete>', item_delete)

# Button Layout
buttonFrame = ttk.Frame(window, width=600)
buttonFrame.pack(pady=5)

# Buttons
importButton = ttk.Button(buttonFrame, text='Import', command=importfunc, style='W.TButton')
importButton.pack(side='left', padx= 10)


continueButton = ttk.Button(buttonFrame, text='Continue', command=continuefunc)
checklist(continueButton,files)
continueButton.pack()

# run
window.mainloop()