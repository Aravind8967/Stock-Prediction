import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense, Input
from keras.optimizers import Adam
import pandas as pd

from src import CompanyDetails
import datetime

class SharePricePrediction:
    def __init__(self, c_name):
        self.c_name = c_name
        self.company_details = CompanyDetails(c_name)

    def str_to_datetime(self, date_str):
        split = date_str.split('-')
        year, month, day = int(split[0]), int(split[1]), int(split[2])
        return datetime.datetime(year=year, month=month, day=day)

    def prediction(self, first_date, last_date):
        share_price_arr = self.company_details.sharePriceRange('4y', '1d')
        share_price_df = pd.DataFrame(share_price_arr)
        share_price_df['Date'] = share_price_df['Date'].apply(self.str_to_datetime)
        share_price_df.index = share_price_df.pop('Date')

        share_price_window_df = self.df_to_windowed_df(share_price_df,first_date_str=first_date, last_date_str=last_date)
        dates, X, y = self.windowed_df_to_date_X_y(share_price_window_df)
        q_80 = int(len(dates) * .8)
        q_90 = int(len(dates) * .9)

        dates_train, X_train, y_train = dates[:q_80], X[:q_80], y[:q_80]

        dates_val, X_val, y_val = dates[q_80:q_90], X[q_80:q_90], y[q_80:q_90]
        dates_test, X_test, y_test = dates[q_90:], X[q_90:], y[q_90:]
        values =  {
            'X_train': X_train,
            'y_train' : y_train,
            'dates_train' : dates_train,
            'dates_val' : dates_val,
            'X_val' : X_val,
            'y_val' : y_val,
            'X_test' : X_test,
            'y_test' : y_test,
            'dates_test' : dates_test
        }

        model = self.train_model(values)
        train_prediction = model.predict(X_train)
        val_prediction = model.predict(X_val).flatten()
        test_prediction = model.predict(X_test).flatten()

        predicted_val = {
            'dates_train' : dates_train,
            'train_prediction' : train_prediction,
            'val_prediction' : val_prediction,
            'test_prediction' : test_prediction,
            'y_train' : y_train,
            'y_val' : y_val,
            'y_test' : y_test
        }

        return predicted_val



    def train_model(self, values):
        model = Sequential([Input((3, 1)),
                            LSTM(64),
                            Dense(32, activation='relu'),
                            Dense(32, activation='relu'),
                            Dense(1)])

        model.compile(loss='mse',
                    optimizer=Adam(learning_rate=0.001),
                    metrics=['mean_absolute_error'])

        model.fit(values['X_train'], values['y_train'], validation_data=(values['X_val'], values['y_val']), epochs=100)
        return model

    def df_to_windowed_df(self, dataframe, first_date_str, last_date_str, n=3):
        first_date = self.str_to_datetime(first_date_str)
        last_date  = self.str_to_datetime(last_date_str)

        target_date = first_date

        dates = []
        X, Y = [], []

        last_time = False
        while True:
            df_subset = dataframe.loc[:target_date].tail(n+1)

            if len(df_subset) != n+1:
                print(f'Error: Window of size {n} is too large for date {target_date}')
                return

            values = df_subset['Close'].to_numpy()
            x, y = values[:-1], values[-1]

            dates.append(target_date)
            X.append(x)
            Y.append(y)

            next_week = dataframe.loc[target_date:target_date+datetime.timedelta(days=7)]
            next_datetime_str = str(next_week.head(2).tail(1).index.values[0])
            next_date_str = next_datetime_str.split('T')[0]
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
        for i in range(0, n):
            X[:, i]
            ret_df[f'Target-{n-i}'] = X[:, i]

        ret_df['Target'] = Y

        return ret_df

    def windowed_df_to_date_X_y(self, windowed_dataframe):
        df_as_np = windowed_dataframe.to_numpy()

        dates = df_as_np[:, 0]

        middle_matrix = df_as_np[:, 1:-1]
        X = middle_matrix.reshape((len(dates), middle_matrix.shape[1], 1))

        Y = df_as_np[:, -1]

        return dates, X.astype(np.float32), Y.astype(np.float32)
