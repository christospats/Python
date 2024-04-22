import tkinter as tk
from tkinter import ttk
from pmoCalculations import pmo_calculation, pmo_signal_buy_sell_report, pmo_plot_total_signals


def calc_button(dataset, text, filename, pmo_results):
    pmo_total_dates_report, pmo_signals_buy_sell = pmo_signal_buy_sell_report(pmo_results, dataset)
    text.insert(tk.END, pmo_signals_buy_sell)
    pmo_plot_total_signals(pmo_results, pmo_total_dates_report, filename)


def pmo_window(dataset, filename):
    # PMO calculations
    pmo_results = pmo_calculation(dataset, 10, 20)

    # window
    window = tk.Tk()
    window.minsize(600, 400)
    window.title('Technical Analysis')
    window.iconbitmap('moneyincrease_118078.ico')

    calc = ttk.Button(window, text='Calculate', command=lambda: calc_button(dataset, text, filename, pmo_results))
    calc.pack()

    text = tk.Text(window)
    text.pack()

    text.insert(tk.END, f'{pmo_results}\n---------Sell or Buy---------\n')

    # run
    window.mainloop()