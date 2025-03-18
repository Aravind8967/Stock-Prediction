import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense

class PredictValues:
    def __init__(self, years, revenue, net_income):
        self.years = years
        self.revenue = revenue
        self.net_income = net_income
        self.n_steps = 3
        self.n_features = 1
        self.model = self.build_model()
        self.train_model()

    def prepare_data(self):
        X, y_revenue, y_net_income = [], [], []
        for i in range(len(self.revenue) - self.n_steps):
            X.append(self.revenue[i:i + self.n_steps])
            y_revenue.append(self.revenue[i + self.n_steps])
            y_net_income.append(self.net_income[i + self.n_steps])
        X = np.array(X).reshape((len(X), self.n_steps, self.n_features))
        y_revenue = np.array(y_revenue)
        y_net_income = np.array(y_net_income)
        return X, y_revenue, y_net_income

    def build_model(self):
        inputs = Input(shape=(self.n_steps, self.n_features))
        lstm_out = LSTM(50, activation='relu')(inputs)
        revenue_output = Dense(1, name='revenue_output')(lstm_out)
        net_income_output = Dense(1, name='net_income_output')(lstm_out)
        model = Model(inputs=inputs, outputs=[revenue_output, net_income_output])
        model.compile(optimizer='adam', loss='mse')
        return model

    def train_model(self):
        X, y_revenue, y_net_income = self.prepare_data()
        self.model.fit(X, {'revenue_output': y_revenue, 'net_income_output': y_net_income}, epochs=300, verbose=1)

    def predict_future(self, input_seq, n_years):
        predictions = []
        current_input = np.array(input_seq).reshape((1, self.n_steps, self.n_features))
        for _ in range(n_years):
            pred_revenue, pred_net_income = self.model.predict(current_input, verbose=0)
            predictions.append((pred_revenue[0][0], pred_net_income[0][0]))
            # Reshape the predicted revenue to match the dimensions: (1, 1, n_feature)
            new_step = pred_revenue.reshape((1, 1, self.n_features))
            # Remove the oldest time step and append the new prediction
            current_input = np.concatenate((current_input[:, 1:, :], new_step), axis=1)
        return predictions

# Example usage:
years = [year for year in range(2015, 2025)]
revenue = [110, 125, 133, 146, 158, 172, 187, 196, 210, 230]
net_income = [10, 12, 13, 15, 16, 17, 19, 20, 22, 24]
input_seq = revenue[-3:]  # Last 3 revenue values as input sequence
pv = PredictValues(years, revenue, net_income)
future_predictions = pv.predict_future(input_seq, 5)
print(future_predictions)
