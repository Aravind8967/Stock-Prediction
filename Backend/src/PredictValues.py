import torch
import os
import random
import pandas as pd
import numpy as np
from .FindValues import FindValues
from neuralprophet.forecaster import NeuralProphet
from neuralprophet.configure import ConfigSeasonality

revenue_model = torch.load('Models/globle_revenue_model.np', weights_only=False, map_location='cpu')
revenue_model.restore_trainer(accelerator="cpu")
income_model = torch.load('Models/globle_income_model.np', weights_only=False, map_location='cpu')
income_model.restore_trainer(accelerator="cpu")


class PredictValues:
    def __init__(self, c_name):
        self.find_values = FindValues(c_name)
        self.c_name = c_name
        self.future_years_arr = []
        self.get_company_details = self.find_values.getCompanyDetails()
        # self.revenue_model = torch.load('Models/globle_revenue_model.np', weights_only=False, map_location='cpu')
        # self.revenue_model.restore_trainer(accelerator="cpu")
        # self.income_model = torch.load('Models/globle_income_model.np', weights_only=False, map_location='cpu')
        # self.income_model.restore_trainer(accelerator="cpu")

    def getFutureRevenueValues(self, future_year=5):
        revenue_df = pd.DataFrame({
            'ds' : pd.to_datetime(self.get_company_details['years'], format='%Y'),
            'y' : self.get_company_details['revenue'],
            'ID' : self.c_name
        })

        future_year = revenue_model.make_future_dataframe(revenue_df, periods=future_year, n_historic_predictions=False)
        revenue_future = revenue_model.predict(future_year)

        self.future_years_arr = revenue_future['ds'].dt.year.astype(int).tolist()
        revenue_values = [round(revenue, 2) for revenue in revenue_future['yhat1'].values]
        return revenue_values
    
    def getFutureIncomeValues(self, future_year=5):
        income_df = pd.DataFrame({
            'ds' : pd.to_datetime(self.get_company_details['years'], format='%Y'),
            'y' : self.get_company_details['income'],
            'ID' : self.c_name
        })

        future_year = income_model.make_future_dataframe(income_df, periods=future_year, n_historic_predictions=False)
        income_future = income_model.predict(future_year)

        income_values = [round(income, 2) for income in income_future['yhat1'].values]
        return income_values
    
    def toFloat(self, arr):
        return [round(float(val), 2) for val in arr]
    
    def toInt(self, arr):
        return [int(val) for val in arr]

    def getFutureValues(self, future_year=5):
        future_revenue = self.getFutureRevenueValues(future_year)
        future_income = self.getFutureIncomeValues(future_year)
        future_values = self.get_company_details
        future_values['future_years'] = self.future_years_arr
        future_values['future_revenue'] = future_revenue
        future_values['future_income'] = future_income
        future_values['future_eps'] = self.find_values.findEPS(future_income)
        future_values['future_roe'] = self.find_values.findROE(future_income)
        future_values['future_opm'] = self.find_values.findOPM(future_revenue, future_income)

        data ={
            'years' : self.toInt(future_values['years']),
            'revenue' : self.toFloat(future_values['revenue']),
            'income' : self.toFloat(future_values['income']),
            'eps' : self.toFloat(future_values['eps']),
            'pe' : int(future_values['pe']),
            'roe' : self.toFloat(future_values['roe']),
            'operating_expence' : self.toFloat(future_values['operating_expence']),
            'profit_margin' : self.toFloat(future_values['profit_margin']),
            'shareholders_equity' : self.toFloat(future_values['shareholders_equity']),
            'outstanding_shares' : float(future_values['outstanding_shares']),
            'future_years' : self.toInt(future_values['future_years']),
            'future_revenue' : self.toFloat(future_values['future_revenue']),
            'future_income' : self.toFloat(future_values['future_income']),
            'future_eps' : self.toFloat(future_values['future_eps']),
            'future_roe' : self.toFloat(future_values['future_roe']),
            'future_opm' : self.toFloat(future_values['future_opm'])
        }
        return data