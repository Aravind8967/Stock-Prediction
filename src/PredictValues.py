import os
import numpy as np
from .APICall import CompanyDetails
from .FindValues import FindValues
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense

class PredictValues:
    def __init__(self, c_name):
        self.c_name = c_name
        self.future_years_arr = []
        self.future_values_arr = []
        self.n_feature = 1
        self.n_steps = 3
        self.previous_values = self.previousValues(self.c_name)
        self.revenue_model = self.modelTrain(self.previous_values['revenue'])
        self.income_model = self.modelTrain(self.previous_values['income'])

    def previousValues(self, c_name):
        previous_values = FindValues(c_name)
        previous_revenue_income = previous_values.getRevenueIncome()
        return {
            'years' : previous_revenue_income['years'], 
            'revenue':previous_revenue_income['revenue'], 
            'income':previous_revenue_income['income']
        }


    def findGrowth(self, val_1, val_2):
        # Calculate percentage growth between two values.
        return round((((100 * val_2) / val_1) - 100), 2)
    
    def prepareData(self, data):
        x_data, y_data = [], []

        for i in range(len(data)):
            end_ix = i + self.n_steps
            if end_ix > len(data) - 1:
                break
            seq_x, seq_y = data[i:end_ix], data[end_ix]
            x_data.append(seq_x)
            y_data.append(seq_y)

        # Convert lists into NumPy arrays.
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

        model.fit(x_data, prepared_data['y_data'], epochs=300, verbose=1)
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
            self.future_years_arr.append(self.previous_values['years'][-1]+current_year)
            current_year += 1

        return {'revenue': future_revenue_arr}

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

        return {'income': future_income_arr}

    def futureRevenueIncome(self, future_year=5):
        future_revenue = self.getFutureRevenueValues(self.previous_values['revenue'][-3:], future_year)
        future_income = self.getFutureIncomeValues(self.previous_values['income'][-3:], future_year)
        return {
            'p_years' : self.previous_values['years'],
            'p_revenue' : self.previous_values['revenue'],
            'p_income': self.previous_values['income'],
            'years': self.future_years_arr,
            'revenue': future_revenue['revenue'],
            'income': future_income['income']
        }