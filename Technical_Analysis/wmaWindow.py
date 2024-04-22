import tkinter as tk
from tkinter import ttk
from calculationsMa import wma_info, signal_buy_sell_report, plot_total_signals

def calc_button(entry_string, dataset, text, filename):
    entry_string = int(entry_string.get())
    wma_a = wma_info(dataset, entry_string)
    WMA_A_total_dates_report, WMA_A_signals_dates = signal_buy_sell_report(dataset, wma_a)
    plot_total_signals(dataset, wma_a, WMA_A_total_dates_report, filename)
    text.insert(tk.END, WMA_A_signals_dates)

def wma_window(dataframe, filename):
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