import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re


# On Balance Volume (OBV) calculation Formula
def obv_calculation(dataset):
  conditional_values = [np.float64("nan")]
  range_value = len(dataset)
  i=0
  while i < (range_value-1):
      tmp_value = dataset['Price'][i]
      tmp_next_value = dataset['Price'][i+1]
      tmp_next_volume = dataset['Volume'][i+1]
      if tmp_next_value > tmp_value:
          conditional_values.append(tmp_next_volume)
      elif tmp_next_value < tmp_value:
          conditional_values.append(-tmp_next_volume)
      else:
          conditional_values.append(0) #όχι στο excel αυτό
      i = i + 1

  conditional_values_df = pd.DataFrame()
  conditional_values_df['IF'] = conditional_values

  tmp_obv = [dataset['Volume'][0]]
  i=0
  while i < (range_value-1):
      tmp_sum = tmp_obv[i] + conditional_values_df['IF'][i+1]
      tmp_obv.append(tmp_sum)
      i = i + 1

  obv_values_df = pd.DataFrame()
  obv_values_df['OBV'] = tmp_obv

  drop_columns = ['Open', 'High', 'Low']
  dset = dataset.drop(columns = drop_columns)

  result_values = pd.DataFrame()
  result_values = pd.concat([dset, conditional_values_df, obv_values_df], axis=1)
  result_values['OBV'] = np.float64(result_values['OBV'].apply("{0:.1f}".format))
  return result_values


# Total Plot PRICE VALUE and OBV RESULTS
def total_plot_obv(dataset,obv_results, filename):
    plt.style.use('fivethirtyeight')
    fig, ax1 = plt.subplots(figsize=(13, 5))

    symbol_name = re.sub("_md", "", filename)

    dataset = dataset.set_index(pd.DatetimeIndex(dataset['Date'].values))
    obv_results = obv_results.set_index(pd.DatetimeIndex(obv_results['Date'].values))

    color = 'tab:red'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price USD ($)', color=color)
    ax1.plot(dataset.index, dataset['Price'], label=f'{symbol_name} Price', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('OBV Values', color=color)  # we already handled the x-label with ax1
    ax2.plot(obv_results.index, obv_results['OBV'], label=f'{symbol_name} OBV', color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # to make sure that the layout is nicely tight
    plt.title(f'Symbol: {symbol_name} [Price History and OBV]')
    plt.show()