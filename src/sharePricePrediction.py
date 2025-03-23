from src import CompanyDetails
from keras.models import Sequential
from keras.layers import LSTM, Dense, Input
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
import numpy as np
import pandas as pd
import datetime

class SharePricePrediction:
    def __init__(self, c_name):
        self.c_name = c_name
        self.company_details = CompanyDetails(c_name)

    def str_to_datetime(self, date_str):
        return datetime.datetime.strptime(date_str, '%Y-%m-%d')


    def prediction(self, first_date_str, last_date_str, pred_range='2y', pred_intvel='1d'):
        # last_date = datetime.datetime.now().date()
        # first_date = last_date - datetime.timedelta(days=365 * 2)
        # first_date_str = str(first_date)
        # last_date_str = str(last_date)
        
        share_price_df = self.company_details.sharePriceRange(pred_range, pred_intvel)
        share_price_df['Date'] = share_price_df['Date'].apply(lambda d: datetime.datetime.strptime(d, '%Y-%m-%d'))
        share_price_df.index = share_price_df.pop('Date')
        windowed_df = self.df_to_windowed_df(share_price_df, first_date_str, last_date_str)
        
        if windowed_df is None:
            raise ValueError("Windowed dataframe creation failed due to insufficient data.")
        
        train_test_validation = self.trainTestValidation(windowed_df)
        return {
                'train_test_validation': train_test_validation, 
                'share_price_df' : share_price_df
            }


    def extractWindow(self, dataframe, target_date, n):
        window = dataframe.loc[:target_date].tail(n+1)
        if len(window) != n+1:
            raise ValueError(f'Window of size {n} is too large for date {target_date}')
        values = window['Close'].to_numpy()
        x = values[:-1]
        y = values[-1]
        return x, y
    
    def getNextTargetDate(self, dataframe, current_date, days_ahead=7):
        # Ensure the dates are sorted
        dates = dataframe.index.sort_values()
        
        if current_date not in dates:
            pos = dates.searchsorted(current_date)
            if pos < len(dates):
                current_date = dates[pos]
            else:
                return None  # No further dates available.
        
        pos = dates.get_loc(current_date)
        # If current_date is the last available date, return None.
        if pos >= len(dates) - 1:
            return None
        
        for next_date in dates[pos+1:]:
            if next_date <= current_date + datetime.timedelta(days=days_ahead):
                return next_date
            else:
                break  # Exit if the date is beyond the window.
        
        # Fallback: return the immediate next available date.
        return dates[pos+1]
    
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

        while True:
            try:
                x, y = self.extractWindow(dataframe, target_date, n)
            except ValueError as e:
                print(e)
                return None

            dates.append(target_date)
            X.append(x)
            Y.append(y)

            # Get the next available target date.
            next_date = self.getNextTargetDate(dataframe, target_date, days_ahead=7)

            # Exit if no further date is available or the next date is beyond the last date.
            if next_date is None or next_date > last_date:
                break

            target_date = next_date

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
        
        early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
        model.fit(x_train, y_train, validation_data=(x_valid, y_valid), epochs=100, callbacks=[early_stop])

        return model