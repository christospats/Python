import tkinter as tk
from tkinter import ttk
from obvCalculations import obv_calculation,total_plot_obv


def obv_func(dataset, calculation, filename):
    total_plot_obv(dataset, calculation, filename)


def obv_window(dataframe, filename):

    calculation = obv_calculation(dataframe)

    # window
    window = tk.Tk()
    window.minsize(600, 400)
    window.title('Technical Analysis')
    window.iconbitmap('moneyincrease_118078.ico')

    #Widgets
    obv = ttk.Button(window, text='OBV plot', command=lambda: obv_func(dataframe, calculation, filename))
    obv.pack()

    text = tk.Text(window)
    text.pack()

    text.insert(tk.END, calculation)


    # window
    window.mainloop()