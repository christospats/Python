import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re


# Signal to Buy or to Sell Report Function
def signal_buy_sell_report(dataset, DATA_B):
    DATA_A = pd.DataFrame(dataset['Price'])
    signal_buy = []
    signal_sell = []
    id = -1
    for i in range(len(dataset)):
        if DATA_A.iloc[:, 0][i] > DATA_B.iloc[:, 0][i]:
            if id != 1:
                signal_buy.append(dataset['Price'][i])
                signal_sell.append(np.nan)
                id = 1
            else:
                signal_buy.append(np.nan)
                signal_sell.append(np.nan)
        elif DATA_A.iloc[:, 0][i] < DATA_B.iloc[:, 0][i]:
            if id != 0:
                signal_buy.append(np.nan)
                signal_sell.append(dataset['Price'][i])
                id = 0
            else:
                signal_buy.append(np.nan)
                signal_sell.append(np.nan)
        else:
            signal_buy.append(np.nan)
            signal_sell.append(np.nan)
    ###
    report_buy_sell = pd.DataFrame()
    report_buy_sell['Date'] = dataset.iloc[:, 0]
    report_buy_sell['signal_buy_price'] = signal_buy
    report_buy_sell['signal_sell_price'] = signal_sell
    ###

    dates_to_buy = report_buy_sell.loc[report_buy_sell['signal_buy_price'] > 0]
    dates_to_buy = dates_to_buy.drop(dates_to_buy.columns[2], axis=1)

    dates_to_sell = report_buy_sell.loc[report_buy_sell['signal_sell_price'] > 0]
    dates_to_sell = dates_to_sell.drop(dates_to_sell.columns[1], axis=1)

    dates_buy_sell = pd.concat([dates_to_buy, dates_to_sell])
    dates_buy_sell.sort_index(inplace=True)
    drop_index = dates_buy_sell.index.tolist()[0]
    dates_buy_sell.set_index('Date', inplace=True)
    drop_index_date = dates_buy_sell.index.tolist()[0]
    dates_buy_sell = dates_buy_sell.drop([drop_index_date], axis=0)
    report_buy_sell.iloc[drop_index, 1:] = np.nan

    return (report_buy_sell, dates_buy_sell)


# Plot Total Signal Report
def plot_total_signals(dataset, data_input, total_dates_report, filename):
    symbol_name = re.sub("_md", "", filename)

    data_input_label = re.sub("Price_", "", data_input.columns[0])

    resize_figure = plt.figure(figsize=(18, 12))
    start_date = dataset['Date'].iloc[0]
    end_date = dataset['Date'].iloc[-1]

    plt.plot(dataset['Price'], label=symbol_name, alpha=0.80, color='violet')
    plt.plot(data_input.iloc[:, 0], label=data_input_label, alpha=0.80, color='red')

    plt.scatter(total_dates_report.index, total_dates_report['signal_buy_price'], label='Buy', marker='^',
                color='forestgreen')
    plt.scatter(total_dates_report.index, total_dates_report['signal_sell_price'], label='Sell', marker='v',
                color='black')

    plt.title('Buy and Sell Signals | Symbol: ' + symbol_name + ' [Price History]')
    plt.xlabel('{} to {}'.format(start_date, end_date))
    plt.ylabel('Price USD')
    plt.legend()
    return plt.show()


# ----------------------------------------------------------- SIMPLE MOVING AVERAGE ---------------------------------------------------------------------------------- #


def sma_info(dataset, window_value):
    tmp_sma = pd.DataFrame()
    tmp_sma['Price'] = dataset['Price'].rolling(window=window_value).mean()
    tmp_sma.columns = ['Price' + '_SMA' + str(window_value)]
    # thewritika panta axrhasta
    # plt.plot(tmp_sma)
    # plt.plot(dataset['Price'])
    # plt.show()
    return tmp_sma


# ----------------------------------------------------------- WEIGHTED MOVING AVERAGE ---------------------------------------------------------------------------------- #


# Generate Weights
def generate_weights(window_value):
    s = 1
    # weights = np.arange(1,window_value+1) #τα βάρη από τιμή 1 έως το πλήθος του window
    weights = np.round(np.random.dirichlet(np.ones(window_value)) * s, 3)
    weights.sort()
    # weights[::-1].sort()
    return weights


# WMA with Plot Function
def wma_info(dataset, window_value):
    input_weights = generate_weights(window_value)
    sum_input_weights = np.sum(input_weights)
    tmp_wma = pd.DataFrame()
    tmp_wma['Price'] = (dataset['Price']
                        .rolling(window=window_value, center=False)
                        .apply(lambda x: np.sum(input_weights * x) / sum_input_weights, raw=False)
                        )
    tmp_wma.columns = ['Price' + '_WMA' + str(window_value)]
    # plt.plot(tmp_wma)
    # plt.plot(dataset['Price'])
    # plt.show()
    return tmp_wma


# ----------------------------------------------------------- EXPONENTIAL MOVING AVERAGE ---------------------------------------------------------------------------------- #

# EMA with Plot Function
def ema_info(dataset, span_value):
  tmp_sma = pd.DataFrame()
  tmp_sma['Price'] = dataset['Price'].rolling(window=span_value).mean()
  tmp_dataset = pd.DataFrame(dataset.iloc[:,1])
  tmp_ema = pd.DataFrame()
  tmp_price = pd.DataFrame(dataset['Price'])
  tmp_ema = tmp_sma + (2/span_value)*(tmp_price-tmp_sma)
  tmp_ema.columns = ['Price'+'_EMA'+ str(span_value)]
  # plt.plot(tmp_ema)
  # plt.plot(tmp_dataset['Price'])
  # plt.show()
  return tmp_ema