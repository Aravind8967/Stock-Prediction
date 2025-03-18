import os
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense

class PredictValues:
    def __init__(self, years, revenue):
        self.years = years
        self.revenue = revenue
        self.future_years_arr = []
        self.future_values_arr = []
        self.n_feature = 1
        self.n_steps = 3
        self.model = self.model_tain()

    def find_growth(self, val_1, val_2):
        # Calculate percentage growth between two values.
        return round((((100 * val_2) / val_1) - 100), 2)
    
    def prepare_data(self):
        x_data, y_data = [], []

        for i in range(len(self.revenue)):
            end_ix = i + self.n_steps
            if end_ix > len(self.revenue) - 1:
                break
            seq_x, seq_y = self.revenue[i:end_ix], self.revenue[end_ix]
            x_data.append(seq_x)
            y_data.append(seq_y)

        # Convert lists into NumPy arrays.
        return {'x_data': np.array(x_data), 'y_data': np.array(y_data)}
    
    def model_tain(self):
        model = Sequential()
        model.add(LSTM(100, activation='relu', return_sequences=True, input_shape=(self.n_steps, self.n_feature)))
        model.add(LSTM(100, activation='relu'))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        
        prepared_data = self.prepare_data()
        x_data = prepared_data['x_data']
        # Reshape the input to [samples, timesteps, features]
        x_data = x_data.reshape((x_data.shape[0], x_data.shape[1], self.n_feature))

        model.fit(x_data, prepared_data['y_data'], epochs=300, verbose=1)
        return model

    def get_future_values(self, x_input, future_year):
        x_input = np.array(x_input)
        temp_input = list(x_input)

        current_year = self.years[-1]
        while current_year <= future_year:
            if len(temp_input) > self.n_steps:
                # If temp_input is longer than n_steps, keep only the latest n_steps values.
                x_input = np.array(temp_input[1:])
                x_input = x_input.reshape((1, self.n_steps, self.n_feature))
                yhat = self.model.predict(x_input, verbose=0)
                temp_input.append(yhat[0][0])
                temp_input = temp_input[1:]
            else:
                x_input = x_input.reshape((1, self.n_steps, self.n_feature))
                yhat = self.model.predict(x_input, verbose=0)
                temp_input.append(yhat[0][0])
            self.future_values_arr.append(round(yhat[0][0], 2))
            self.future_years_arr.append(current_year)
            current_year += 1

        return {'values': self.future_values_arr, 'years': self.future_years_arr}

# Example usage:
if __name__ == '__main__':
    years = [year for year in range(2015, 2025)]
    revenue = [110, 100, 130, 120, 160, 140, 180, 160, 200]
    x_input = [110, 100, 130, 120]
    pv = PredictValues(years, revenue)
    forecast_results = pv.get_future_values(x_input, 2030)
    print(forecast_results)
