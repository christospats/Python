import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re


# Simple SMA with Plot Function
def sma_info(dataset, window_value, plot_values):
  tmp_sma = pd.DataFrame()
  tmp_sma['Price'] = dataset['Price'].rolling(window=window_value).mean()
  tmp_sma.columns = ['Price'+'_SMA'+ str(window_value)]
  if plot_values == True:
      plt.plot(tmp_sma)
      plt.plot(dataset['Price'])
      plt.show()
  return tmp_sma


# Price Momentum Oscillator (PMO) calculation Formula
def pmo_calculation(dataset, window_value_A, window_value_B):
    plot_values = False
    drop_columns = ['Open', 'High', 'Low', 'Volume']
    dset = dataset.drop(columns = drop_columns)
    SMA_A = sma_info(dataset,window_value_A,plot_values)
    SMA_B = sma_info(dataset,window_value_B,plot_values)
    PMO = pd.DataFrame(SMA_A.iloc[:,0] - SMA_B.iloc[:,0])
    PMO.columns = ['T'+str(window_value_A)+"-"+str(window_value_B)]
    result_values = pd.DataFrame()
    result_values = pd.concat([dset, SMA_A, SMA_B, PMO], axis=1)
    return result_values


#Βήμα 5 | PMO - Signal to Buy or to Sell Report Function
def pmo_signal_buy_sell_report(data_input, dataset):
    ###
    check_signal = []
    range_a = data_input.isna().sum().iloc[4]
    for i in range(range_a):
        check_signal.append(np.nan)

    c = range_a-1
    range_b = len(data_input)-1
    for i in range(c,range_b):
        if data_input.iloc[:,4][i+1] < 0:
            check_signal.append(-1)
        else:
            check_signal.append(1)

    check_signal = pd.DataFrame(check_signal)
    check_signal.columns = ['flag']
    ###

    ###
    signals = []
    range_c = check_signal.isna().sum().iloc[0]+1
    for i in range(range_c):
        signals.append(np.nan)

    range_value = len(check_signal)
    i=range_c
    while i < (range_value):
        tmp_value = check_signal['flag'][i-1]
        tmp_next_value = check_signal['flag'][i]
        if tmp_next_value == tmp_value:
            signals.append(np.nan)
        else:
            signals.append(tmp_next_value)
        i = i + 1
    signals = pd.DataFrame(signals)
    signals.columns = ["Buy_Sell_Flag"]
    ###

    ###
    drop_columns = [2,3,4] #['Price_SMA10', 'Price_SMA20', 'T10-20']
    tmp_dataset = data_input.drop(data_input.columns[drop_columns],axis=1)
    signal_prices = pd.DataFrame()
    signal_prices = pd.concat([tmp_dataset,signals], axis=1)
    ###

    ###
    DATA_A = pd.DataFrame(signal_prices.iloc[:,1]) #Price (close values)
    DATA_B = pd.DataFrame(signal_prices.iloc[:,2]) #Flag Buy or Sell (PMO)
    length_dataset = len(signal_prices)

    signal_buy = []
    signal_sell = []
    flag_id = 0
    for i in range(length_dataset):
        if DATA_B.iloc[:,0][i] == 1:
            if flag_id != 2:
                signal_buy.append(DATA_A['Price'][i])
                signal_sell.append(np.nan)
                flag_id = 2
            else:
                signal_buy.append(np.nan)
                signal_sell.append(np.nan)
        elif  DATA_B.iloc[:,0][i] == -1:
            if flag_id !=1:
                signal_buy.append(np.nan)
                signal_sell.append(DATA_A['Price'][i])
                flag_id = 1
            else:
                signal_buy.append(np.nan)
                signal_sell.append(np.nan)
        else:
            signal_buy.append(np.nan)
            signal_sell.append(np.nan)
    ###

    ###
    report_buy_sell = pd.DataFrame()
    report_buy_sell['Date'] = dataset.iloc[:,0]
    report_buy_sell['signal_buy_price'] = signal_buy
    report_buy_sell['signal_sell_price'] = signal_sell
    ###

    ###
    dates_to_buy = report_buy_sell.loc[report_buy_sell['signal_buy_price']>0]
    dates_to_buy = dates_to_buy.drop(dates_to_buy.columns[2],axis=1)
    dates_to_sell = report_buy_sell.loc[report_buy_sell['signal_sell_price']>0]
    dates_to_sell = dates_to_sell.drop(dates_to_sell.columns[1],axis=1)
    ###

    ###
    dates_buy_sell = pd.concat([dates_to_buy, dates_to_sell])
    dates_buy_sell.sort_index(inplace=True)
    dates_buy_sell.set_index('Date', inplace = True)
    ###

    return (report_buy_sell, dates_buy_sell)


# Plot Total Signal Report (PMO)
def pmo_plot_total_signals(metric_results,total_dates_report, filename):
    symbol_name = re.sub("_md", "", filename)

    sma_a_name = metric_results.columns[2]
    sma_b_name = metric_results.columns[3]
    sma_a_label = re.sub("Price_", "", sma_a_name)
    sma_b_label = re.sub("Price_", "", sma_b_name)

    # Create subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 10), sharex=True)

    # Plot Price and SMAs
    metric_results = metric_results.set_index(pd.DatetimeIndex(metric_results['Date'].values))
    ax1.plot(metric_results['Price'], label=symbol_name, alpha=0.80, color='violet')
    ax1.plot(metric_results[sma_a_name], label=sma_a_label, alpha=0.80, color='red')
    ax1.plot(metric_results[sma_b_name], label=sma_b_label, alpha=0.80, color='green')

    # Check Null Signals for Price and SMAs
    total_dates_report = total_dates_report.set_index(pd.DatetimeIndex(metric_results['Date'].values))
    if len(total_dates_report) != total_dates_report.isnull().sum().sum() / 2:
        ax1.scatter(total_dates_report.index, total_dates_report['signal_buy_price'], label='Buy', marker='^',
                    color='forestgreen')
        ax1.scatter(total_dates_report.index, total_dates_report['signal_sell_price'], label='Sell', marker='v',
                    color='black')

    ax1.set_title('Buy and Sell Signals | Symbol: ' + symbol_name + ' [Price History]')
    ax1.set_ylabel('Price USD')
    ax1.legend(loc=2, prop={'size': 7})
    ax1.set_xlim([total_dates_report.index[0], total_dates_report.index[-1]])

    # Plot PMO
    pmo_name = metric_results.columns[4]
    ax2.plot(metric_results[pmo_name], label=symbol_name, alpha=0.80, color='red')
    ax2.axhline(0, linestyle='dotted', color='red')
    ax2.set_ylabel(pmo_name + ' PMO values')
    ax2.set_xlim([total_dates_report.index[0], total_dates_report.index[-1]])

    plt.tight_layout()
    plt.show()