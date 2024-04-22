import tkinter as tk
from tkinter import ttk
from functions import (md_csv_dataset, remove_chars)
from smaWindow import sma_window
from wmaWindow import wma_window
from expoWindow import expo_window
from rsiWindow import rsi_window
from obvWindow import obv_window
from williamsWindow import williams_window
from rocWindow import roc_window
from pmoWindow import pmo_window

def smafunc(notebook, filepaths):
    file_name = remove_chars(notebook)
    current_tab_index = notebook.index("current")
    dataframe = md_csv_dataset(filepaths[current_tab_index])
    # print(dataframe)
    sma_window(dataframe, file_name)


def wmafunc(notebook, filepaths):
    file_name = remove_chars(notebook)
    current_tab_index = notebook.index("current")
    dataframe = md_csv_dataset(filepaths[current_tab_index])
    wma_window(dataframe, file_name)


def expfunc(notebook, filepaths):
    file_name = remove_chars(notebook)
    current_tab_index = notebook.index("current")
    dataframe = md_csv_dataset(filepaths[current_tab_index])
    expo_window(dataframe, file_name)


def rsifunc(notebook, filepaths):
    file_name = remove_chars(notebook)
    current_tab_index = notebook.index("current")
    dataframe = md_csv_dataset(filepaths[current_tab_index])
    rsi_window(dataframe, file_name)


def obvfunc(notebook, filepaths):
    file_name = remove_chars(notebook)
    current_tab_index = notebook.index("current")
    dataframe = md_csv_dataset(filepaths[current_tab_index])
    obv_window(dataframe, file_name)


def williamsfunc(notebook, filepaths):
    file_name = remove_chars(notebook)
    current_tab_index = notebook.index("current")
    dataframe = md_csv_dataset(filepaths[current_tab_index])
    williams_window(dataframe, file_name)


def rocfunc(notebook, filepaths):
    file_name = remove_chars(notebook)
    current_tab_index = notebook.index("current")
    dataframe = md_csv_dataset(filepaths[current_tab_index])
    roc_window(dataframe, file_name)


def pmofunc(notebook, filepaths):
    file_name = remove_chars(notebook)
    current_tab_index = notebook.index("current")
    dataframe = md_csv_dataset(filepaths[current_tab_index])
    pmo_window(dataframe, file_name)


def secondScreen(files, filepaths):
    # window.destroy()
    scdwindow = tk.Tk()
    scdwindow.title("Technical Analysis")
    scdwindow.minsize(600, 400)
    scdwindow.iconbitmap('moneyincrease_118078.ico')

    # Tabs
    notebook = ttk.Notebook(scdwindow)

    for i in files.get_children():
        tabi = ttk.Frame(notebook)
        notebook.add(tabi, text=f'{files.item(i)["values"]}')
        sma = ttk.Button(tabi, text='Simple Moving Average', command=lambda: smafunc(notebook, filepaths))
        wma = ttk.Button(tabi, text='Weighted Moving Average', command=lambda: wmafunc(notebook, filepaths))
        ema = ttk.Button(tabi, text='Exponential Moving Average', command=lambda: expfunc(notebook, filepaths))
        rsi = ttk.Button(tabi, text='RSI', command=lambda: rsifunc(notebook, filepaths))
        obv = ttk.Button(tabi, text='OBV', command=lambda: obvfunc(notebook, filepaths))
        macd = ttk.Button(tabi, text='MACD')
        pmo = ttk.Button(tabi, text='PMO', command=lambda: pmofunc(notebook, filepaths))
        roc = ttk.Button(tabi, text='ROC', command=lambda: rocfunc(notebook, filepaths))
        williams = ttk.Button(tabi, text='Williams', command=lambda: williamsfunc(notebook, filepaths))
        sma.pack()
        wma.pack()
        ema.pack()
        rsi.pack()
        obv.pack()
        macd.pack()
        pmo.pack()
        roc.pack()
        williams.pack()
        print(files.item(i)['values'])

    notebook.pack()

    # run
    scdwindow.mainloop()
