import datetime
from .APICall import CompanyDetails
import pandas as pd
import numpy as np
import torch
from neuralprophet.forecaster import NeuralProphet
from neuralprophet.configure import ConfigSeasonality

torch.serialization.add_safe_globals([NeuralProphet, ConfigSeasonality])
model = torch.load('Models/globle_shareprice_model.np', weights_only=False, map_location='cpu')
model.restore_trainer(accelerator="cpu")

class SharePricePrediction:
    def __init__(self, company_name):
        self.c_name = company_name
        self.company_details = CompanyDetails(self.c_name)
        self.previous_share_price = []

    def getFutureSharePrice(self, future_years):
        share_price = self.company_details.sharePriceRange(period='6y')
        self.previous_share_price = share_price[['Date', 'Close']].to_dict(orient='records')
        share_price_df = pd.DataFrame({
            'ds' : pd.to_datetime(share_price['Date']),
            'y' : share_price['Close'],
            'ID' : self.c_name
        })
        c_techincal_details = self.company_details.techincalDetails()
        c_min_price = c_techincal_details['line_data']['support2']


        c_future_days = model.make_future_dataframe(share_price_df, periods=(365 * future_years), n_historic_predictions=False)
        c_forcast = model.predict(c_future_days)
        
        c_forcast = c_forcast.rename(columns={'ds':'Date'}) 
        c_forcast['Date'] = pd.to_datetime(c_forcast['Date'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
        c_forcast['Close'] = c_forcast['yhat1'].rolling(window=7, center=True, min_periods=1).mean().clip(lower=c_min_price).round(2)
        c_forcast = c_forcast[['Date', 'Close']]
        c_forcast = c_forcast.to_dict(orient='records')
        return c_forcast
    

    def SharePrice(self, future_years=5):
        future_share_price = self.getFutureSharePrice(future_years=future_years)
        previous_share_price = self.previous_share_price
        return {
            'previous_share_price' : previous_share_price,
            'future_share_price' : future_share_price
        }

    
if __name__ == '__main__':
    c_name = 'ITC'
    future = SharePricePrediction(company_name=c_name)
    print(future.SharePrice())