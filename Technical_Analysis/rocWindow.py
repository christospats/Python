import tkinter as tk
from tkinter import ttk
from rocCalculations import roc_calculation, roc_signal_buy_sell_report,roc_plot_total_signals


def calc_button(entry, dataset, text, filename):
    entry_string = int(entry.get())
    results = roc_calculation(dataset, entry_string)
    text.insert(tk.END, results)
    text.insert(tk.END, '\n---------Sell or Buy---------\n')
    roc_total_dates_report, roc_signals_buy_sell = roc_signal_buy_sell_report(results, dataset)
    text.insert(tk.END, roc_signals_buy_sell)
    roc_plot_total_signals(results, roc_total_dates_report, filename)



def roc_window(dataframe, filename):
    # window
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

    entry = ttk.Entry(frame)
    entry.pack(side='left')

    calc = ttk.Button(frame, text='Calculate', command=lambda: calc_button(entry, dataframe, text, filename))
    calc.pack(side='left')

    # run
    window.mainloop()