import tkinter as tk
from tkinter import ttk
from rsiCalculations import plot_dataset,total_plot_rsi, calculate_rsi, plot_rsi, rsi_signals_buy_sell


def price_button(dataframe, filename):
    plot_dataset(dataframe, filename)


def inticator_button(dataframe, filename, rsi):
    plot_rsi(dataframe, rsi, filename)


def total_button(dataframe, filename, rsi):
    total_plot_rsi(dataframe, rsi, filename)


def rsi_window(dataframe, filename):
    # Values needed
    rsi = calculate_rsi(dataframe)

    # window
    window = tk.Tk()
    window.minsize(600,400)
    window.title('Technical Analysis')
    window.iconbitmap('moneyincrease_118078.ico')

    # widgets
    price = ttk.Button(window, text='Price Diagram', command=lambda: price_button(dataframe, filename))
    inticator = ttk.Button(window, text='Inticator', command=lambda: inticator_button(dataframe, filename, rsi))
    total = ttk.Button(window, text='Total Plots', command=lambda: total_button(dataframe, filename, rsi))

    price.pack()
    inticator.pack()
    total.pack()

    text = tk.Text(window)
    text.pack()

    # Insert Sell or Buy
    signal_buy, signal_sell = rsi_signals_buy_sell(dataframe, rsi)
    text.insert(tk.END, signal_buy)
    text.insert(tk.END, signal_sell)

    # run
    window.mainloop()
