from .APICall import CompanyDetails
from .FindValues import FindValues
from .PredictValues import PredictValues


class Analyse:
    def __init__(self, c_name):
        self.c_name = c_name
        self.company_details = CompanyDetails(self.c_name)
        self.predict_values = PredictValues(self.c_name)
        self.future_revenue_income = self.predict_values.futureRevenueIncome()

    def getAPIValues(self):
        revenue_income = self.company_details.getRevenueIncome()
        return {
            'years':revenue_income['years'],
            'revenue':revenue_income['revenue'],
            'income':revenue_income['income']
        }
    
    def RevenueIncomeAnalyse(self):
        return {
            'p_years': self.future_revenue_income['p_years'],
            'p_revenue' : self.future_revenue_income['p_revenue'],
            'p_income' : self.future_revenue_income['p_income'],
            'years' : self.future_revenue_income['years'],
            'revenue' : self.future_revenue_income['revenue'],
            'income' : self.future_revenue_income['income']
        }
    
    def ROEAnalyse(self):
        prev_roe = self.company_details.roe(self.future_revenue_income['p_income'], self.future_revenue_income)
        



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