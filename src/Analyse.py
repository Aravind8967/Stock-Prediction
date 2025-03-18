from .APICall import CompanyDetails
from .FindValues import FindValues
from .PredictValues import PredictValues


class Analyse:
    def __init__(self, c_name):
        self.c_name = c_name

    def getAPIValues(self):
        details = CompanyDetails(self.c_name)
        revenue_income = details.getRevenueIncome()
        return {
            'years':revenue_income['years'],
            'revenue':revenue_income['revenue'],
            'income':revenue_income['income']
        }
    
    def predictionValues(self):
        predict_values = PredictValues(self.c_name)
        future_revenue_income = predict_values.futureRevenueIncome()
        return {
            'p_years': future_revenue_income['p_years'],
            'p_revenue' : future_revenue_income['p_revenue'],
            'p_income' : future_revenue_income['p_income'],
            'years' : future_revenue_income['years'],
            'revenue' : future_revenue_income['revenue'],
            'income' : future_revenue_income['income']
        }


if __name__ == '__main__':
    c_name = 'ITC'
    analyse = Analyse(c_name)
    current_values = analyse.getAPIValues()
    future_values = analyse.predictionValues()
    for c_value in current_values:
        print(f'Previous {c_value} : {current_values[c_value]}')

    print('=============================================================================')

    for f_value in future_values:
        print(f'Future {f_value} : {future_values[f_value]}')