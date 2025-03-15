from analysis import Company_details

def share_price_arr(c_name):
    yfinance_data = Company_details(c_name)
    share_price_arr = yfinance_data.share_price_range('1mo', '1d')
    return share_price_arr

def company_details(c_name):
    yfinance_data = Company_details(c_name)
    company_info = yfinance_data.company_data()
    return company_info

        

if __name__ == '__main__':
    c_names = ['RELIANCE','HDFCBANK', 'TCS', 'KOTAKBANK', 'BAJFINANCE', 'BAJAJFINSV', 'SBILIFE']

    for c_name in c_names:
        details = company_details(c_name)
        print(f'========================== {c_name} ==============================')
        for data in details:
            print(f'{data} : {details[data]}')
        print('===================================================================')