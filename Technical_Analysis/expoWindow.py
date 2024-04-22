import tkinter as tk
from tkinter import ttk
from calculationsMa import ema_info, signal_buy_sell_report, plot_total_signals


def calc_button(entry_string, dataset, text, filename):
    entry_string = int(entry_string.get())
    ema_a = ema_info(dataset, entry_string)
    EMA_A_total_dates_report, EMA_A_signals_dates = signal_buy_sell_report(dataset, ema_a)
    plot_total_signals(dataset, ema_a, EMA_A_total_dates_report, filename)
    text.insert(tk.END, EMA_A_signals_dates)



def expo_window(dataframe, file_name):
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

    calc = ttk.Button(frame, text='Calculate', command=lambda: calc_button(entry, dataframe, text, file_name))
    calc.pack(side='left')

    # run
    window.mainloop()