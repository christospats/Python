import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import Sequential, layers
from copy import deepcopy

df = pd.read_csv('MSFT.csv')
print(df)

def str_to_datetime(s):
    split = s.split('-')
    year, month, day = int(split[0]), int(split[1]), int(split[2])
    return datetime.datetime(year= year, month=month, day=day)

df['Date'] = df['Date'].apply(str_to_datetime)
print(df['Date'])

df.index = df.pop('Date')

plt.plot(df.index,df['Close'])
plt.show()


def df_to_windowed_df(dataframe, first_date_str, last_date_str, n=3):
    first_date = str_to_datetime(first_date_str)
    last_date = str_to_datetime(last_date_str)

    target_date = first_date

    dates = []
    X, Y = [], []

    last_time = False
    while True:
        df_subset = dataframe.loc[:target_date].tail(n + 1)

        if len(df_subset) != n + 1:
            print(f'Error: Window of size {n} is too large for date {target_date}')
            return

        features = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        values = df_subset[features].to_numpy()
        x, y = values[:-1], values[-1][3]  # Target is Close price of the next day

        dates.append(target_date)
        X.append(x)
        Y.append(y)

        next_week = dataframe.loc[target_date:target_date + datetime.timedelta(days=1)]  # Next day
        next_datetime_str = str(next_week.head(1).index.values[0])
        next_date_str = next_datetime_str.split(' ')[0]
        year_month_day = next_date_str.split('-')
        year, month, day = year_month_day
        next_date = datetime.datetime(day=int(day), month=int(month), year=int(year))

        if last_time:
            break

        target_date = next_date

        if target_date == last_date:
            last_time = True

    ret_df = pd.DataFrame({})
    ret_df['Target Date'] = dates

    X = np.array(X)
    for i, feature in enumerate(features):
        for j in range(0, n):
            ret_df[f'{feature}-Target-{n - j}'] = X[:, j, i]

    ret_df['Target'] = Y

    return ret_df

def windowed_df_to_X_y(windowed_dataframe):
    df_as_np = windowed_dataframe.to_numpy()

    dates = df_as_np[:, 0]

    num_features = (windowed_dataframe.shape[1] - 2) // window_size

    X = np.zeros((len(dates), window_size, num_features))
    for i in range(num_features):
        X[:, :, i] = df_as_np[:, 1 + i*window_size:1 + (i+1)*window_size]

    Y = df_as_np[:, -1]

    return dates, X.astype(np.float32), Y.astype(np.float32)

window_size = 3  # Number of days to consider in the window

# Modify the function call to include all features and predict tomorrow's Close price
windowed_df = df_to_windowed_df(df, '1986-03-18', '2024-04-05', n=window_size)
print(windowed_df)

dates, X, y = windowed_df_to_X_y(windowed_df)

print(dates.shape, X.shape, y.shape)

q_80 = int(len(dates)* .8)
q_90 = int(len(dates)* .9)

dates_train, X_train, y_train = dates[:q_80], X[:q_80], y[:q_80]

dates_val, X_val, y_val = dates[q_80: q_90], X[q_80:q_90], y[q_80:q_90]
dates_test, X_test, y_test = dates[q_90:], X[q_90:], y[q_90:]

plt.plot(dates_train, y_train)
plt.plot(dates_val, y_val)
plt.plot(dates_test, y_test)

plt.legend(['Train', 'Validation', 'Test'])
plt.show()


model = Sequential([
    layers.Input((window_size, 6)),  # 6 features: Open, High, Low, Close, Adj Close, Volume
    layers.LSTM(300),  # Set return_sequences=False since you're not stacking LSTM layers
    layers.Dense(32, activation='relu'),
    layers.Dense(32, activation='relu'),
    layers.Dense(1)
])

model.compile(loss='mse', optimizer= Adam(learning_rate=0.001), metrics=['mean_absolute_error'])

model.fit(X_train, y_train, validation_data=(X_val,y_val), epochs=100)

train_predictions = model.predict(X_train).flatten()

plt.plot(dates_train, train_predictions)
plt.plot(dates_train, y_train)
plt.legend(['Training Predictions', 'Training Observations'])
plt.show()

val_predictions = model.predict(X_val).flatten()

plt.plot(dates_val, val_predictions)
plt.plot(dates_val, y_val)
plt.legend(['Validation Predictions', 'Vallidation Observations'])
plt.show()

test_predictions = model.predict(X_test).flatten()

plt.plot(dates_test, test_predictions)
plt.plot(dates_test, y_test)
plt.legend(['Testing Predictions', 'Testing Observations'])
plt.show()

plt.plot(dates_train, train_predictions)
plt.plot(dates_train, y_train)
plt.plot(dates_val, val_predictions)
plt.plot(dates_val, y_val)
plt.plot(dates_test, test_predictions)
plt.plot(dates_test, y_test)
plt.legend(['Training Predictions',
            'Training Observations',
            'Validation Predictions',
            'Validation Observations',
            'Testing Predictions',
            'Testing Observations'])
plt.show()

recursive_predictions = []
recursive_dates = np.concatenate([dates_val, dates_test])

for target_date in recursive_dates:
    last_window = deepcopy(X_train[-1])
    next_prediction = model.predict(np.array([last_window])).flatten()
    recursive_predictions.append(next_prediction)
    last_window[-1] = next_prediction

plt.plot(dates_train, train_predictions)
plt.plot(dates_train, y_train)
plt.plot(dates_val, val_predictions)
plt.plot(dates_val, y_val)
plt.plot(dates_test, test_predictions)
plt.plot(dates_test, y_test)
plt.plot(recursive_dates, recursive_predictions)
plt.legend(['Training Predictions',
            'Training Observations',
            'Validation Predictions',
            'Validation Observations',
            'Testing Predictions',
            'Testing Observations',
            'Recursive Predictions'])

plt.show()