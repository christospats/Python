import pandas as pd
import matplotlib.pyplot as plt
import re


# Williams(%R) and Stochastic(%K) calculation Formula
def williams_stochastic_calculation(dataset, window_value):
    tmp_a = pd.DataFrame()
    tmp_a['High'] = dataset['High'].rolling(window=window_value).max()
    tmp_a.columns = ['Highest_High'+'_W'+ str(window_value)]

    tmp_b = pd.DataFrame()
    tmp_b['Low'] = dataset['Low'].rolling(window=window_value).min()
    tmp_b.columns = ['Lowest_Low'+'_W'+ str(window_value)]

    #tmp_stochastic  = pd.DataFrame(100+tmp_williams.iloc[:,0])
    tmp_stochastic  = pd.DataFrame(((dataset['Price'] - tmp_b.iloc[:,0]) / (tmp_a.iloc[:,0]-tmp_b.iloc[:,0])) * (100))
    tmp_stochastic.columns = ['Stochastic_(%K)'+'_W'+ str(window_value)]
    tmp_stochastic = round(tmp_stochastic,3)

    #tmp_williams = pd.DataFrame(((tmp_a.iloc[:,0] - dataset['Price']) / (tmp_a.iloc[:,0]-tmp_b.iloc[:,0])) * (-100))
    tmp_williams = pd.DataFrame(tmp_stochastic.iloc[:,0]-100)
    tmp_williams.columns = ['Williams_(%R)'+'_W'+ str(window_value)]
    tmp_williams = round(tmp_williams,3)

    result_values = pd.DataFrame()
    result_values = pd.concat([dataset, tmp_a, tmp_b, tmp_williams], axis=1)
    drop_columns = ['Volume']
    result_values = result_values.drop(columns = drop_columns)

    return result_values


# Plot Williams(%R)
def total_plot_metrics(metric_results, filename):
    symbol_name = re.sub("_md", "", filename)

    # Create a single figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), sharex=True)

    # Plot Symbol Price on the first subplot
    metric_results = metric_results.set_index(pd.DatetimeIndex(metric_results['Date'].values))
    ax1.plot(metric_results['Price'], label=symbol_name, alpha=0.80, color='violet')
    ax1.set_title('Symbol: ' + symbol_name + ' [Price History]')
    ax1.set_ylabel('Price USD')

    # Plot Williams (%R) on the second subplot
    willimas_name = metric_results.columns[7]
    ax2.plot(metric_results[willimas_name], label=willimas_name, alpha=0.80, color='red')
    ax2.axhline(-20, linestyle='dotted', color='forestgreen')
    ax2.axhline(-80, linestyle='dotted', color='red')
    ax2.set_ylabel(willimas_name + ' values')

    # Set x-axis limit for both subplots
    ax1.set_xlim([metric_results.index[0], metric_results.index[-1]])
    ax2.set_xlim([metric_results.index[0], metric_results.index[-1]])

    # Add legend to both subplots
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper left')

    plt.tight_layout()
    plt.show()
    ax2.set_xlim([metric_results.index[0], metric_results.index[len(metric_results)-1]])
    #plt.legend(loc=2, prop={'size': 7})
    return
