from .APICall import CompanyDetails
import numpy as np


class FindValues:
    def __init__(self, c_name):
        self.c_name = c_name

    def getRevenueIncome(self):
        details = CompanyDetails(self.c_name)
        revene_income = details.getRevenueIncome()
        previous_values = self.previousValues(revene_income['years'], revene_income['revenue'], revene_income['income'])

        return {
            'years': previous_values['years'], 
            'revenue': previous_values['revenue'], 
            'income': previous_values['income']
        }

    def previousValues(self, years, revenue, income, target_start_year = 2012):
        revenue_growth = []
        income_growth = []

        for i in range(1, len(revenue)):
            revenue_growth.append(round((revenue[i] / revenue[i-1] - 1) * 100, 2))
            income_growth.append(round((income[i] / income[i-1] - 1) * 100, 2))

        revenue_cycle = [revenue_growth[-1], revenue_growth[-2], revenue_growth[-3]]
        income_cycle = [income_growth[-1], income_growth[-2], income_growth[-3]]

        ext_years, ext_revenue, ext_income = list(years), list(revenue), list(income)
        current_year = ext_years[0]
        cycle_index = 0
        
        while current_year > target_start_year:
            rev_growth_pct = revenue_cycle[cycle_index % len(revenue_cycle)]
            inc_growth_pct = income_cycle[cycle_index % len(income_cycle)]
            
            new_rev = round(ext_revenue[0] / (1 + rev_growth_pct / 100), 2)
            new_inc = round(ext_income[0] / (1 + inc_growth_pct / 100), 2)
            
            new_year = current_year - 1
            
            ext_years.insert(0, new_year)
            ext_revenue.insert(0, new_rev)
            ext_income.insert(0, new_inc)
            
            current_year = new_year
            cycle_index += 1

        return {
            'years': ext_years, 
            'revenue': ext_revenue, 
            'income': ext_income
        }


def main_1(): 

    c_names = ['RELIANCE','HDFCBANK', 'TCS', 'KOTAKBANK', 'BAJFINANCE', 'BAJAJFINSV', 'SBILIFE']

    for c_name in c_names:
        details = CompanyDetails(c_name)
        print(f'========================== {c_name} ==============================')
        for data in details:
            print(f'{data} : {details[data]}')
        print('===================================================================') 
