import pandas as pd
import numpy as np
import re


def remove_chars(notebook):
    selected_tab_index = notebook.index(notebook.select())
    selected_tab_name = notebook.tab(selected_tab_index, "text")
    characters_to_remove = "[']"
    modified_name = selected_tab_name
    for i in characters_to_remove:
        modified_name = modified_name.replace(i, "")
    print(modified_name)
    return modified_name


# Βήμα SOS
# Direct CSV to CSV_md (investing.com)
def md_csv_dataset(filename):
    chart = pd.read_csv(filename,sep=',')
    n_col = len(chart.columns)
    chart = chart.drop(chart.columns[n_col - 1], axis=1)

    if len(chart.columns) < 6:
        chart['Volume'] = 0
        id = 1
    else:
        id = 0

    chart.columns = ['Date', 'Price',
                     'Open', 'High',
                     'Low', 'Volume']

    # Μορφή Ημερομηνίας
    chart.Date = pd.to_datetime(chart.Date).dt.strftime('%m-%d-%Y')

    chart = chart.replace(',', '', regex=True)
    chart = chart.replace('%', '', regex=True)
    chart.iloc[:, 1:6] = chart.iloc[:, 1:6].replace('-', '0', regex=True)

    chart['Date'] = chart['Date'].astype('datetime64[ns]')
    chart['Date'] = chart['Date'].dt.date
    chart['Price'] = chart['Price'].astype(np.float64)
    chart['Open'] = chart['Open'].astype(np.float64)
    chart['High'] = chart['High'].astype(np.float64)
    chart['Low'] = chart['Low'].astype(np.float64)

    if id != 1:
        for i in range(len(chart)):
            tmp_value = chart.iloc[i, 5]
            if tmp_value != re.sub("K", "", tmp_value):
                chart.iloc[i, 5] = np.float64(re.sub("K", "", tmp_value)) * 1000
            elif tmp_value != re.sub("M", "", tmp_value):
                chart.iloc[i, 5] = np.float64(re.sub("M", "", tmp_value)) * 1000000
            elif tmp_value != re.sub("B", "", tmp_value):
                chart.iloc[i, 5] = np.float64(re.sub("B", "", tmp_value)) * 1000000000
        chart['Volume'] = chart['Volume'].astype(np.float64)
    else:
        # update 111220
        chart[
            'Volume'] = 0  # Υπήρχε θέμα με το volume οπότε το θέτω με μηδέν ( 0 ) όταν δεν υπάρχει η στήλη από το investing.com
        # md_col = len(chart.columns)
        # chart = chart.drop(chart.columns[md_col-1],axis=1)

    chart.sort_values(by=['Date'], inplace=True, ascending=True)

    # update 081220
    chart.index = range(len(chart['Date']))

    return chart

