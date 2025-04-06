import os
import random
import numpy as np
from .FindValues import FindValues
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense

class PredictValues:
    def __init__(self, c_name):
        self.find_values = FindValues(c_name)
        self.c_name = c_name
        self.future_years_arr = []
        self.n_feature = 1
        self.n_steps = 3
        self.get_company_details = self.find_values.getCompanyDetails()
        self.revenue_model = self.modelTrain(self.get_company_details['revenue'])
        self.income_model = self.modelTrain(self.get_company_details['income'])

    def prepareData(self, data):
        x_data, y_data = [], []

        for i in range(len(data)):
            end_ix = i + self.n_steps
            if end_ix > len(data) - 1:
                break
            seq_x, seq_y = data[i:end_ix], data[end_ix]
            x_data.append(seq_x)
            y_data.append(seq_y)

        return {
            'x_data': np.array(x_data), 
            'y_data': np.array(y_data)
        }
    
    def modelTrain(self, data):
        model = Sequential()
        model.add(LSTM(100, activation='relu', return_sequences=True, input_shape=(self.n_steps, self.n_feature)))
        model.add(LSTM(100, activation='relu'))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        
        prepared_data = self.prepareData(data)
        x_data = prepared_data['x_data']
        # Reshape the input to [samples, timesteps, features]
        x_data = x_data.reshape((x_data.shape[0], x_data.shape[1], self.n_feature))

        model.fit(x_data, prepared_data['y_data'], epochs=10, verbose=1)
        return model

    def getFutureRevenueValues(self, x_input, future_year=5):
        x_input = np.array(x_input)
        temp_input = list(x_input)

        future_revenue_arr = []

        current_year = 1
        while current_year <= future_year:
            if len(temp_input) > self.n_steps:
                # If temp_input is longer than n_steps, keep only the latest n_steps values.
                x_input = np.array(temp_input[1:])
                x_input = x_input.reshape((1, self.n_steps, self.n_feature))
                yhat = self.revenue_model.predict(x_input, verbose=0)
                temp_input.append(yhat[0][0])
                temp_input = temp_input[1:]
            else:
                x_input = x_input.reshape((1, self.n_steps, self.n_feature))
                yhat = self.revenue_model.predict(x_input, verbose=0)
                temp_input.append(yhat[0][0])
            future_revenue_arr.append(round(yhat[0][0], 2))
            self.future_years_arr.append(self.get_company_details['years'][-1]+current_year)
            current_year += 1

        return future_revenue_arr
    
    def getfutureSharePrice(self, eps_arr):
        pe = self.get_company_details['pe']
        if pe <= 0:
            pe = 3
        share_price = []
        for eps in eps_arr:
            share_price.append(round(eps * random.randint(pe, pe+5), 2))
        return share_price

    def getFutureIncomeValues(self, x_input, future_year=5):
        x_input = np.array(x_input)
        temp_input = list(x_input)

        future_income_arr = []

        current_year = 1
        while current_year <= future_year:
            if len(temp_input) > self.n_steps:
                # If temp_input is longer than n_steps, keep only the latest n_steps values.
                x_input = np.array(temp_input[1:])
                x_input = x_input.reshape((1, self.n_steps, self.n_feature))
                yhat = self.income_model.predict(x_input, verbose=0)
                temp_input.append(yhat[0][0])
                temp_input = temp_input[1:]
            else:
                x_input = x_input.reshape((1, self.n_steps, self.n_feature))
                yhat = self.income_model.predict(x_input, verbose=0)
                temp_input.append(yhat[0][0])
            future_income_arr.append(round(yhat[0][0], 2))
            current_year += 1

        return future_income_arr

    def npToval(self, arr):
        return [round(float(val), 2) for val in arr]
    

    def getFutureValues(self, future_year=5):
        future_revenue = self.getFutureRevenueValues(self.get_company_details['revenue'][-3:], future_year)
        future_income = self.getFutureIncomeValues(self.get_company_details['income'][-3:], future_year)
        future_values = self.get_company_details
        future_values['future_years'] = self.future_years_arr
        future_values['future_revenue'] = self.npToval(future_revenue)
        future_values['future_income'] = self.npToval(future_income)
        future_values['future_eps'] = self.npToval(self.find_values.findEPS(future_income))
        future_values['future_roe'] = self.npToval(self.find_values.findROE(future_income))
        future_values['future_opm'] = self.npToval(self.find_values.findOPM(future_revenue, future_income))
        future_values['future_price'] = self.npToval(self.getfutureSharePrice(future_values['future_eps']))
        return future_values