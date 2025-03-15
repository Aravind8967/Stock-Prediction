import os
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense

class Predict_values:
    def __init__(self, years, revenue, model_filename="saved_model.h5"):
        self.years = years
        self.revenue = revenue
        self.feature_years_arr = []
        self.feature_revenue_arr = []
        self.n_feature = 1
        self.n_steps = 3
        self.model_filename = model_filename

        # Check if a trained model already exists on disk
        if os.path.exists(self.model_filename):
            # Load the saved model to avoid retraining
            self.model = load_model(self.model_filename)
            print("Loaded saved model.")
        else:
            # Train the model as no saved model is found
            self.model = self.model_tain()
            # Save the trained model for future use
            self.model.save(self.model_filename)
            print("Trained and saved a new model.")

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
        # Build a Sequential LSTM model with two LSTM layers and one Dense output.
        model = Sequential()
        model.add(LSTM(100, activation='relu', return_sequences=True, input_shape=(self.n_steps, self.n_feature)))
        model.add(LSTM(100, activation='relu'))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        
        # Prepare the data for training.
        prepared_data = self.prepare_data()
        x_data = prepared_data['x_data']
        # Reshape the input to [samples, timesteps, features]
        x_data = x_data.reshape((x_data.shape[0], x_data.shape[1], self.n_feature))

        # Train the model for 300 epochs (adjust epochs as needed).
        model.fit(x_data, prepared_data['y_data'], epochs=500, verbose=1)
        return model

    def get_feature_values(self, x_input, feature_year):
        # Convert input into a numpy array and then to a list for prediction iterations.
        x_input = np.array(x_input)
        temp_input = list(x_input)

        # Start forecasting from the last available year
        current_year = self.years[-1]
        while current_year <= feature_year:
            if len(temp_input) > self.n_steps:
                # If temp_input is longer than n_steps, keep only the latest n_steps values.
                x_input = np.array(temp_input[1:])
                x_input = x_input.reshape((1, self.n_steps, self.n_feature))
                yhat = self.model.predict(x_input, verbose=0)
                temp_input.append(yhat[0][0])
                temp_input = temp_input[1:]
            else:
                # If we have exactly n_steps values.
                x_input = x_input.reshape((1, self.n_steps, self.n_feature))
                yhat = self.model.predict(x_input, verbose=0)
                temp_input.append(yhat[0][0])
            # Save the forecasted revenue and corresponding year.
            self.feature_revenue_arr.append(round(yhat[0][0], 2))
            self.feature_years_arr.append(current_year)
            current_year += 1

        return {'feature_revenue': self.feature_revenue_arr, 'feature_years': self.feature_years_arr}

# Example usage:
if __name__ == '__main__':
    years = [year for year in range(2015, 2025)]
    revenue = [110, 100, 130, 120, 160, 140, 180, 160, 200]
    x_input = [110, 100, 130, 120]
    pv = Predict_values(years, revenue)
    forecast_results = pv.get_feature_values(x_input, 2030)
    print(forecast_results)
