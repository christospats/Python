import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# ROC calculation Formula
def roc_calculation(dataset,p):
    drop_columns = ['Open', 'High', 'Low', 'Volume']
    dset = dataset.drop(columns = drop_columns)

    roc_values = []
    for i in range(p):
        roc_values.append(np.nan)
    range_a = len(dset)

    t = p #start point
    for i in range(t,range_a):
        tmp_roc = ((dset.iloc[i,1] / dset.iloc[i-p,1])-1)*100
        roc_values.append(tmp_roc)
    roc_values = pd.DataFrame(roc_values)
    roc_values.columns = ['ROC'+'_P'+ str(p)]

    result_values = pd.DataFrame()
    result_values = pd.concat([dset, roc_values], axis=1)
    return result_values


# ROC - Signal to Buy or to Sell Report Function
def roc_signal_buy_sell_report(data_input, dataset):
    ###
    range_a = data_input.isna().sum().iloc[2]

    check_signal = []
    for i in range(range_a):
        check_signal.append(np.nan)

    c = range_a-1
    range_b = len(data_input)-1
    for i in range(c,range_b):
        if data_input.iloc[:,2][i+1] < 0:  # με βάση το ROC column
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
    drop_columns = [2]
    tmp_dataset = data_input.drop(data_input.columns[drop_columns],axis=1)
    signal_prices = pd.DataFrame()
    signal_prices = pd.concat([tmp_dataset,signals], axis=1)
    ###

    ###
    DATA_A = pd.DataFrame(signal_prices.iloc[:,1]) #Price (close values)
    DATA_B = pd.DataFrame(signal_prices.iloc[:,2]) #Flag Buy or Sell (ROC)
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


# Plot Total Signal Report (ROC)
def roc_plot_total_signals(metric_results,total_dates_report, filename):
    symbol_name = re.sub("_md", "", filename)

    # Create subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 10), sharex=True)

    # Plot Price and Signals
    metric_results = metric_results.set_index(pd.DatetimeIndex(metric_results['Date'].values))
    ax1.plot(metric_results['Price'], label=symbol_name, alpha=0.80, color='violet')

    total_dates_report = total_dates_report.set_index(pd.DatetimeIndex(metric_results['Date'].values))

    # Check Null Signals
    if len(total_dates_report) != total_dates_report.isnull().sum().sum() / 2:
        ax1.scatter(total_dates_report.index, total_dates_report['signal_buy_price'], label='Buy', marker='^',
                    color='forestgreen')
        ax1.scatter(total_dates_report.index, total_dates_report['signal_sell_price'], label='Sell', marker='v',
                    color='black')

    ax1.set_title('Buy and Sell Signals | Symbol: ' + symbol_name + ' [Price History]')
    ax1.set_ylabel('Price USD')
    ax1.legend(loc=2, prop={'size': 7})

    # Plot ROC
    roc_name = metric_results.columns[2]
    ax2.plot(metric_results[roc_name], label=roc_name, alpha=0.80, color='red')
    ax2.axhline(0, linestyle='dotted', color='black')

    ax2.set_ylabel(roc_name + ' values')

    # Set x-axis limits
    ax1.set_xlim([total_dates_report.index[0], total_dates_report.index[-1]])
    ax2.set_xlim([total_dates_report.index[0], total_dates_report.index[-1]])

    plt.tight_layout()
    plt.show()