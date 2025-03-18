from APICall import CompanyDetails
import numpy as np

def sharePriceArr(c_name):
    yfinance_data = CompanyDetails(c_name)
    share_price_arr = yfinance_data.share_price_range('1mo', '1d')
    return share_price_arr

def companyDetails(c_name):
    yfinance_data = CompanyDetails(c_name)
    company_info = yfinance_data.company_data()
    return company_info


def previousValues(years, revenue, income, target_start_year = 2012):
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
        
        # To back-calculate the previous year's value:
        # current_value = previous_value * (1 + growth/100)
        # Therefore, previous_value = current_value / (1 + growth/100)
        new_rev = round(ext_revenue[0] / (1 + rev_growth_pct / 100), 2)
        new_inc = round(ext_income[0] / (1 + inc_growth_pct / 100), 2)
        
        # Determine the previous year.
        new_year = current_year - 1
        
        # Insert the newly calculated values at the beginning of the lists.
        ext_years.insert(0, new_year)
        ext_revenue.insert(0, new_rev)
        ext_income.insert(0, new_inc)
        
        # Update the current year and cycle index.
        current_year = new_year
        cycle_index += 1

    return {'years': ext_years, 'revenue': ext_revenue, 'net_income': ext_income}



def main_1(): 

    c_names = ['RELIANCE','HDFCBANK', 'TCS', 'KOTAKBANK', 'BAJFINANCE', 'BAJAJFINSV', 'SBILIFE']

    for c_name in c_names:
        details = CompanyDetails(c_name)
        print(f'========================== {c_name} ==============================')
        for data in details:
            print(f'{data} : {details[data]}')
        print('===================================================================') 


if __name__ == '__main__':
    c_name = 'SBILIFE'
    data = CompanyDetails(c_name)
    print('years : ', data['years'])
    print('revenue : ', data['revenue'])
    print('income : ', data['net_income'])

    print('=============================================================')

    prev_ext = previousValues(data['years'], data['revenue'], data['net_income'])
    print('previous revenue : ', prev_ext['years'])
    print('previous revenue : ', prev_ext['revenue'])
    print('previous net_income : ', prev_ext['net_income'])
