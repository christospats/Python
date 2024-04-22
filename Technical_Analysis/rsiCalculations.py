import pandas as pd
import matplotlib.pyplot as plt
import re

# ----------------------------------------------------------------------------------------------------------------------------------------- #

# Plot Dataset Function
def plot_dataset(dataset, filename):
    plt.style.use('fivethirtyeight')
    symbol_name = re.sub("_md", "", filename)
    resize_figure = plt.figure(figsize=(12.5,5))
    #start_date = dataset['Date'].iloc[0]
    #end_date = dataset['Date'].iloc[-1]
    dataset = dataset.set_index(pd.DatetimeIndex(dataset['Date'].values))

    plt.plot(dataset['Price'], label = symbol_name, alpha = 0.80, color = 'violet')

    plt.title('Symbol: ' + symbol_name + ' [Price History]')
    #plt.xlabel('{} to {}'.format(start_date, end_date))
    plt.ylabel('Price USD ($)')
    #plt.legend()
    return plt.show()

# RSI Dataset Calculation

def calculate_rsi(dataset, period_value=14):
    dataset = dataset.set_index(pd.DatetimeIndex(dataset['Date'].values))

    dd = dataset['Price'].diff(1)
    dd = dd.dropna()
    up_values = dd.copy()
    down_values = dd.copy()
    up_values[up_values < 0] = 0
    down_values[down_values > 0] = 0

    average_gain = up_values.rolling(window=period_value).mean()
    average_loss = abs(down_values.rolling(window=period_value).mean())
    rs_value = average_gain / average_loss
    rsi_value = 100 - (100 / (1 + rs_value))

    return rsi_value


# RSI plot Calculator
def plot_rsi(dataset, rsi_value, filename):
    plt.style.use('fivethirtyeight')
    plt.figure(figsize=(12.5, 5))
    symbol_name = re.sub("_md", "", filename)
    plt.plot(rsi_value, label=symbol_name, alpha=0.80, color='violet')
    plt.title(f'Symbol: {symbol_name} [RSI PLOT]')
    plt.ylabel('RSI Values (0 - 100)')
    plt.legend()
    plt.show()


# Total Plot PRICE VALUE and RSI RESULTS
def total_plot_rsi(dataset,rsi_result,filename):
    plt.style.use('fivethirtyeight')
    symbol_name = re.sub("_md", "", filename)

    # Ensure the dataset's Date column is the index for plotting
    dataset = dataset.set_index(pd.DatetimeIndex(dataset['Date'].values))

    # Creating a figure with two subplots (2 rows, 1 column)
    fig, axs = plt.subplots(2, 1, figsize=(13, 10))  # Increase the figure size to accommodate both plots comfortably

    # Plotting Price on the first subplot
    axs[0].plot(dataset['Price'], label=symbol_name, alpha=0.80, color='violet')
    axs[0].set_title(f'Symbol: {symbol_name} [Price History]')
    axs[0].set_ylabel('Price USD ($)')

    # Plotting RSI on the second subplot
    axs[1].plot(rsi_result, label=f'{symbol_name} RSI', alpha=0.80, color='violet')
    axs[1].axhline(30, linestyle='dotted', color='forestgreen')
    axs[1].axhline(70, linestyle='dotted', color='red')
    axs[1].set_title('RSI PLOT')
    axs[1].set_ylabel('RSI Values (0 - 100)')

    # Automatically adjust subplot params so that the subplot(s) fits in to the figure area
    plt.tight_layout()
    plt.show()


# RSI SIGNALS Buy or Sell
def rsi_signals_buy_sell(dataset,rsi_result):
  signal_rsi = "nothing"
  signals_rsi = []
  for i in range(len(rsi_result)):
          if rsi_result.iloc[i] < 30:
                    signal_rsi = 'buy'
          elif rsi_result.iloc[i] > 70:
                    signal_rsi = 'sell'
          else:
                   signal_rsi = "nothing"
          signals_rsi.append(signal_rsi)

  rsi_signals_report = pd.DataFrame()
  rsi_signals_report["RSI_VALUES"] = rsi_result
  rsi_signals_report["SIGNALS"] = signals_rsi
  dates_to_buy = rsi_signals_report.loc[rsi_signals_report['SIGNALS']=='buy']
  dates_to_sell = rsi_signals_report.loc[rsi_signals_report['SIGNALS']=='sell']
  return dates_to_buy,dates_to_sell