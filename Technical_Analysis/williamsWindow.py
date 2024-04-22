import tkinter as tk
from tkinter import ttk
from williamsCalculations import williams_stochastic_calculation, total_plot_metrics


def calc_button(entry, dataset, text, filename):
    entry_string = int(entry.get())
    result = williams_stochastic_calculation(dataset, entry_string)
    total_plot_metrics(result, filename)
    text.insert(tk.END, result)


def williams_window(dataframe, filename):
    window = tk.Tk()
    window.minsize(600, 400)
    window.title('Technical Analysis')
    window.iconbitmap('moneyincrease_118078.ico')

    label = ttk.Label(window, text='Enter the days')
    label.pack()
    frame = ttk.Frame(window)
    frame.pack()

    text = tk.Text(window)
    text.pack()

    default_value = '14'
    entry = ttk.Entry(frame)
    entry.insert(0, default_value)
    entry.pack(side='left')

    calc = ttk.Button(frame, text='Calculate', command=lambda: calc_button(entry, dataframe, text, filename))
    calc.pack(side='left')

    # run
    window.mainloop()
