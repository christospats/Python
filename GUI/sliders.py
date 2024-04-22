import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

#window
window = tk.Tk()
window.title("Sliders")
window.geometry("600x400")

#slider
scale_int = tk.DoubleVar(value=15)
scale = ttk.Scale(window, command=lambda value: progress.stop(), from_=0, to=25, length=300, variable=scale_int)
scale.pack()

#progressbar
progress = ttk.Progressbar(window, variable=scale_int, maximum=25)
progress.pack()

# progress.start()

#ScrollText
scroll = scrolledtext.ScrolledText(window,width=100, height= 5)
scroll.pack()

#Excercise
ex_int = tk.IntVar()
progressBar = ttk.Progressbar(window, orient='vertical', variable=ex_int)
progressBar.pack()

progressBar.start()
label = ttk.Label(window, textvariable=ex_int)
label.pack()

ex_slider = ttk.Scale(window,variable=ex_int, from_=0, to=100)
ex_slider.pack()


#run
window.mainloop()