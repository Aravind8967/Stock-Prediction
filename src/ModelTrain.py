import datetime
from APICall import CompanyDetails
import pandas as pd
import numpy as np
import tensorflow as tf
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Input, Dropout
from keras.regularizers import l2
kernel_regularizer=l2(0.01)
from keras.optimizers import Adam

class ModelTrain:
    def __init__(self, company_list, model_name, window_size=5, price_range='25y'):
        self.c_list = company_list
        self.window_size = window_size
        self.price_range = price_range
        self.companies_df = self.loadCompany()
        self.x_all, self.y_all = self.loadAndCombineData()
        self.model = self.trainModel(model_name)
    
    def loadCompany(self):
        companies_df = []
        for company in self.c_list:
            company_details = CompanyDetails(company)
            share_price_df = company_details.sharePriceRange(self.price_range)
            share_price_df['Date'] = share_price_df['Date'].apply(lambda d: datetime.datetime.strptime(d, '%Y-%m-%d')).sort_index()
            share_price_df.index = share_price_df.pop('Date')
            companies_df.append(share_price_df)
            print(f'{company} added to Companies_df')
        
        print("All companies share-price data added to the companies df list")
        return companies_df

    def createWindowsForCompanies(self, company_df):
        data_x, data_y = [], []

        company_df = company_df.sort_index()
        close_vals = company_df['Close'].values
        ema_vals = company_df['ema200'].values

        for i in range(len(company_df) - self.window_size):
            x_window = []
            for window in range(self.window_size):
                x_window.append([close_vals[i + window], ema_vals[i + window]])
            
            target = close_vals[i + self.window_size]
            data_x.append(x_window)
            data_y.append(target)
        
        print('Creating the window for the companies done.')

        return np.array(data_x), np.array(data_y)
    
    def loadAndCombineData(self):
        x_combined, y_combined = [], []

        for df in self.companies_df:
            x, y = self.createWindowsForCompanies(df)
            if len(x) > 0:
                x_combined.append(x)
                y_combined.append(y)
        
        if len(x_combined) == 0:
            raise ValueError("No data found after window creation.")

        x_all = np.concatenate(x_combined, axis=0)
        y_all = np.concatenate(y_combined, axis=0)

        print('All the companies share price combained into x_all and y_all')

        return x_all, y_all
    
    def trainModel(self, model_name):
        num_samples = len(self.x_all)

        train_end = int(num_samples * 0.8)
        valid_end   = int(num_samples * 0.9)

        x_train, y_train = self.x_all[:train_end], self.y_all[:train_end]
        x_valid, y_valid   = self.x_all[train_end:valid_end], self.y_all[train_end:valid_end]
        x_test, y_test  = self.x_all[valid_end:], self.y_all[valid_end:]

        model = Sequential()

        model.add(LSTM(units=120, activation='relu', return_sequences=True, input_shape=(self.x_all.shape[1], self.x_all.shape[2]), kernel_regularizer=l2(0.01), recurrent_dropout=0.2))

        model.add(LSTM(units=64, activation='relu', return_sequences=True, kernel_regularizer=l2(0.01), recurrent_dropout=0.2))

        model.add(LSTM(units=32, activation='relu', return_sequences=False, kernel_regularizer=l2(0.01), recurrent_dropout=0.2))

        model.add(Dense(32, activation='relu', kernel_regularizer=l2(0.01)))
        model.add(Dropout(0.2))

        model.add(Dense(16, activation='relu', kernel_regularizer=l2(0.01)))
        model.add(Dropout(0.2))

        # final output layer
        model.add(Dense(1, activation='linear'))

        model.compile(
            loss='mse',
            optimizer=Adam(learning_rate=0.001),
            metrics=['mae']
        )

        model.fit(
            x_train, y_train,
            validation_data=(x_valid, y_valid),
            epochs=10,
            batch_size=32
        )

        test_loss, test_mae = model.evaluate(x_test, y_test)
        print(f"Test MSE: {test_loss:.4f}, Test MAE: {test_mae:.4f}")
        
        # below command save the model to the current dir
        model.save(f'Models/{model_name}.keras')

        print(f'{model_name} saved to current dir')
        return model
    
    def getModel(self):
        return self.model
    
if __name__ == '__main__':
    c_list = ['ITC', 'ONGC']
    model = ModelTrain(company_list=c_list, model_name='Aravind_test2', price_range='2y')
    print({'get model':model.getModel()})