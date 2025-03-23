from src import CompanyDetails
from keras.models import Sequential
from keras.layers import LSTM, Dense, Input
from keras.optimizers import Adam
import numpy as np
import pandas as pd
import datetime

class SharePricePrediction:
    def __init__(self, c_name):
        self.c_name = c_name
        self.company_details = CompanyDetails(c_name)

    def str_to_datetime(self, date_str):
        year, month, day = map(int, date_str.split('-'))
        return datetime.datetime(year=year, month=month, day=day)

    def prediction(self, pred_range='2y', pred_intvel='1d'):
        
        share_price_df = self.company_details.sharePriceRange(pred_range, pred_intvel)
        share_price_df['Date'] = share_price_df['Date'].apply(self.str_to_datetime)
        share_price_df.index = share_price_df.pop('Date')
        windowed_df = self.df_to_windowed_df(share_price_df, '2023-03-21', '2025-03-21')
        
        train_test_validation = self.trainTestValidation(windowed_df)
        return train_test_validation

    def extractWindow(self, dataframe, target_date, n):
        window = dataframe.loc[:target_date].tail(n+1)
        if len(window) != n+1:
            raise ValueError(f'Window of size {n} is too large for date {target_date}')
        values = window['Close'].to_numpy()
        x = values[:-1]
        y = values[-1]
        return x, y

    def getNextTargetDate(self, dataframe, current_date, days_ahead=7):
        next_week = dataframe.loc[current_date:current_date + datetime.timedelta(days=days_ahead)]
        next_datetime_str = str(next_week.head(2).tail(1).index.values[0])
        next_date_str = next_datetime_str.split('T')[0]
        next_date = datetime.datetime.strptime(next_date_str, '%Y-%m-%d')
        return next_date

    def buildWindowedDF(self, dates, X, Y, n):
        ret_df = pd.DataFrame()
        ret_df['Target Date'] = dates
        X = np.array(X)
        for i in range(n):
            ret_df[f'Target-{n-i}'] = X[:, i]
        ret_df['Target'] = Y
        return ret_df

    def df_to_windowed_df(self, dataframe, first_date_str, last_date_str, n=3):
        first_date = self.str_to_datetime(first_date_str)
        last_date = self.str_to_datetime(last_date_str)

        target_date = first_date
        dates = []
        X, Y = [], []
        last_time = False

        while True:
            try:
                x, y = self.extractWindow(dataframe, target_date, n)
            except ValueError as e:
                print(e)
                return None

            dates.append(target_date)
            X.append(x)
            Y.append(y)

            # Determine the next target date (within a week ahead).
            next_date = self.getNextTargetDate(dataframe, target_date, days_ahead=7)

            if last_time:
                break

            target_date = next_date

            if target_date == last_date:
                last_time = True

        return self.buildWindowedDF(dates, X, Y, n)
    
    def windowTodateXY(self, window_df):
        # Converts every row of df to an array 
        df_as_np = window_df.to_numpy()
        # df_as_np o/p = [[Timestamp('2023-03-21 00:00:00') 361.41 355.82 358.9 357.15]..........]

        # first colume of window_df is about dates
        # : = hole df_as_np array's [0]'th val means dates colume
        # o/p = [Timestamp('2023-03-21 00:00:00')]
        dates = df_as_np[:, 0]

        # it is about window_df[share_price_values]
        # : = hole df_as_np array's [1st_colume] to [last_colume]
        # o/p = [361.41 355.82 358.9] accept target value
        middle_matrix = df_as_np[:, 1:-1]

        '''
            o/p = [[[361.41]
                    [355.82]
                    [358.9]]
                    .........
                    .........]]    
        '''
        data_x = middle_matrix.reshape((len(dates), middle_matrix.shape[1], 1))
        
        # below line gives output with only df_values
        # : means hole [0] end of err    -1 = second part of values
        # o/p = [357.15 357.91 360.65 358.81 360.23]
        data_y = df_as_np[:, -1]
        return dates, data_x.astype(np.float32), data_y.astype(np.float32)
    
    def trainTestValidation(self, windowed_df):
        dates, data_x, data_y = self.windowTodateXY(windowed_df)

        q_80 = int(len(dates) * .8)
        q_90 = int(len(dates) * .9)

        # Training dataset
        dates_train, x_train, y_train = dates[:q_80], data_x[:q_80], data_y[:q_80]

        # Validation dataset
        dates_valid, x_valid, y_valid = dates[q_80:q_90], data_x[q_80:q_90], data_y[q_80:q_90]

        # testing dataset
        dates_test, x_test, y_test = dates[q_90:], data_x[q_90:], data_y[q_90:]

        model = self.model_train(x_train, y_train, x_valid, y_valid)

        train_prediction = model.predict(x_train).flatten()

        valid_prediction = model.predict(x_valid).flatten()

        test_prediction = model.predict(x_test).flatten()

        return {
            'dates_train' : dates_train,
            'y_train' : y_train,
            'train_prediction' : train_prediction,
            'dates_valid' : dates_valid,
            'y_valid' : y_valid,
            'valid_prediction' : valid_prediction,
            'dates_test' : dates_test,
            'y_test' : y_test,
            'test_prediction' : test_prediction
        }

    def model_train(self, x_train, y_train, x_valid, y_valid):
        model = Sequential([Input((3, 1)),
                            LSTM(64),
                            Dense(32,activation='relu'),
                            Dense(32, activation='relu'),
                            Dense(1)])
        
        model.compile(loss='mse',
                      optimizer=Adam(learning_rate=0.001),
                      metrics=['mean_absolute_error'])

        model.fit(x_train, y_train, validation_data=(x_valid, y_valid), epochs=100)
        return model