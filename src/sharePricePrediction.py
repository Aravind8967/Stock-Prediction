import datetime
from APICall import CompanyDetails
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Input
from keras.optimizers import Adam

class SharePricePrediction:
    def __init__(self, company_name, model_name, price_range=5, window_size=5):
        self.c_name = company_name
        self.model_name = model_name
        self.price_range = price_range
        self.window_size = window_size
        self.company_details = CompanyDetails(self.c_name)
        self.share_price_df = self.sharePriceDF()
        self.model = self.findModel()
    
    def findModel(self):
        try:
            self.model = load_model(f'Models/{self.model_name}.keras')
            return self.model
        except (OSError, ValueError) as e:
            print(f"Error loading model '{self.model_name}': {e}")
            raise RuntimeError("Model not found, exiting class.") from e

    def sharePriceDF(self):
        share_price_df = self.company_details.sharePriceRange(f'{self.price_range}y')
        share_price_df['Date'] =share_price_df['Date'].apply(lambda d: datetime.datetime.strptime(d, '%Y-%m-%d')).sort_index()
        share_price_df.index = share_price_df.pop('Date')
        return share_price_df.sort_index()
    
    def createWindowForInstance(self):
        data_x = []
        close_vals = self.share_price_df['Close'].values
        ema_vals = self.share_price_df['ema200'].values

        for i in range(len(self.share_price_df) - self.window_size):
            windows = []
            for window in range(self.window_size):
                windows.append([close_vals[i + window], ema_vals[i + window]])
            data_x.append(windows)

        return np.array(data_x)
    
    def sharePricePrediction(self):
        window_for_instance = self.createWindowForInstance()
        price_prediction = self.model.predict(window_for_instance)
        prediction_dates = self.share_price_df.index[self.window_size:]
        result_df = pd.DataFrame()
        result_df['Date'] = prediction_dates
        result_df['Close'] = price_prediction.flatten()
        result_df['ema200'] = price_prediction.flatten()
        result_df.set_index('Date', inplace=True)
        return result_df
    
    def futurePricePrediction(self, future_years=5):
        last_row = self.share_price_df.iloc[-1]
        know_date = self.share_price_df.index[-1]
        last_close = last_row['Close']
        last_ema = last_row['ema200']
        last_window = self.share_price_df[['Close', 'ema200']].tail(self.window_size).to_numpy()

        future_months = []
        current_date = self.share_price_df.index[-1]

        # crating the future month
        for _ in range(future_years * 12):
            year, month = current_date.year, current_date.month
            month += 1
            if month > 12:
                month = 1
                year += 1
            current_date = datetime.datetime(year=year, month=month, day=1)
            future_months.append(current_date)

        # finding future shareprices
        alpha = 2 / 201.0
        future_close = []
        future_ema = []

        current_window = last_window.copy()
        for _ in range(future_years * 12):
            input_data = np.expand_dims(current_window, axis=0)
            pred_close = self.model.predict(input_data)
            pred_close_val = pred_close.flatten()[0]
            last_ema = current_window[-1, 1]
            new_ema = (pred_close_val - last_ema) * alpha + last_ema

            future_close.append(pred_close_val)
            future_ema.append(new_ema)

            new_row = np.array([[pred_close_val, new_ema]])
            current_window = np.vstack([current_window[1:], new_row])

        future_price_df = pd.DataFrame()
        future_price_df['Date'] = future_months
        future_price_df['Close'] = future_close
        future_price_df['ema200'] = future_ema

        return future_price_df
    
    def futureSharePrice(self, future_years=5):
        previous_share_price = self.sharePricePrediction()
        future_share_price = self.futurePricePrediction(future_years=future_years)
        return {
            'previous_share_price' : previous_share_price,
            'future_share_price' : future_share_price
        }

    
if __name__ == '__main__':
    c_name = 'ITC'
    future = SharePricePrediction(company_name=c_name, model_name='Aravind_test2')
    print(future.futureSharePrice())