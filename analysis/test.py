from datetime import date, datetime, timedelta
import numpy as np
import yfinance as yf
from tradingview_ta import TA_Handler, Interval
import pandas as pd
import requests


class analysis:
    def __init__(self, name):
        self.company_name = f'{name}.NS'
        self.yf_api_fetch = yf.Ticker(self.company_name)
        self.company_info = self.yf_api_fetch.info
        self.company_symbol = name
        self.tradingview_data = self.tradingview_connect(name)

    def tradingview_connect(self, symbol):
        handler = TA_Handler(
            symbol=symbol,
            screener="india",
            exchange="NSE",
            interval='1d'
        )
        analysis = handler.get_analysis()
        summary = analysis.summary
        oscillator  = analysis.oscillators
        indicators = analysis.indicators

        data = {
            "summery": summary,
            "oscillator": oscillator,
            "indicators": indicators
        }
        return data
   
    def share_price(self):
        return self.company_info['currentPrice']
    
    def share_price_range(self, period='max', interval='1d'):
        stock = self.yf_api_fetch
        share_price_arr = stock.history(period=period, interval=interval)
        if share_price_arr.empty : return []
        filtered_data = []    
        for index, row in share_price_arr.iterrows():
            date = index.strftime('%Y-%m-%d')
            share_price = round(row['Close'], 2)
            volume = row['Volume']
            filtered_data.append({
                'time': date,
                'share_price': share_price,
                'volume': volume
            })
        return filtered_data

    # using for company_section in webpage 
    def company_data(self):
        row_data_tradingview = self.tradingview_data['indicators']
        row_data_yfinance = self.yf_api_fetch.info
        data = {
            'share_price': row_data_yfinance['currentPrice'],
            'change':round(row_data_tradingview['change'], 2),
            'c_name':row_data_yfinance['shortName'],
            'c_symbol':row_data_yfinance['symbol'].split('.')[0]
        }
        return data

class yfinance:
    def __init__(self, name):
        self.company_name = f'{name}.NS'
        self.yf_api_fetch = yf.Ticker(self.company_name)
        self.company_info = self.yf_api_fetch.info
        self.company_symbol = name

    def share_price(self):
        data = self.company_info
        if 'currentPrice' in data:
            return data['currentPrice']
        else:
            return None
    # need to work on it detailes saved on notes.
    def calender(self):
        data = self.yf_api_fetch
        calender = data.calendar
        return calender

    def get_nearest_shareprice(self, date):
        date = datetime.strptime(date, '%Y-%m-%d').date()
        start_date = (date - timedelta(days=5)).strftime('%Y-%m-%d')  # start 10 days before the date
        end_date = (date + timedelta(days=5)).strftime('%Y-%m-%d')
        shareprice = self.yf_api_fetch.history(start=start_date, end=end_date)
        return round((shareprice['Close'].iloc[0]), 2)

    def company_details(self):
        company_info = self.company_info
        def helper(key):
            if key in company_info:
                return company_info[key]
            else:
                return 1
        data = {
            'bussiness': helper('longBusinessSummary'),
            'share_price': helper('currentPrice'),
            'change_num': round(helper('currentPrice') - helper('previousClose'), 2),
            'change_percent': round((100 * (helper('currentPrice')-helper('previousClose'))) / helper('currentPrice'), 2),
            'c_name': helper('shortName'),
            'c_symbol': self.company_symbol, 
            'website': helper('website'),
            'marketcap':round(helper('marketCap')/10000000),
            'industry' : helper('industry'),
            'sector':helper('sector'),
            'pe' : round(helper('trailingPE'), 2),
            'pb' : round(helper('priceToBook'), 2),
            'eps' : helper('trailingEps'),
            'targetprice' : helper('targetHighPrice'),
            'fifty2_week_low' : helper('fiftyTwoWeekLow'),
            'fifty2_week_high' : helper('fiftyTwoWeekHigh'),
            'divident_yield' : round(helper('dividendYield')*100, 2) if helper('dividendYield') else 0,
            'bookvalue' : round(helper('bookValue'), 2),
            'earning_growth' : round(helper('earningsGrowth')*100, 2) if helper('earningsGrowth') else 0,
            'revenue_growth' : round((helper('revenueGrowth') * 100), 2) if helper('earningsGrowth') else 0,
            'total_cash' : round(helper('totalCash')/1000000),
            'total_debt': round(helper('totalDebt')/1000000),
            'total_revenue':round(helper('totalRevenue')/1000000),
            'day_low' : helper('dayLow'),
            'day_high' : helper('dayHigh'),
            'profit_margin' : round((helper('profitMargins')*100),2),
        }
        return data
    # operating profit margin
    def opm(self, revenue, net_income):
        opm = []
        for rev, ni in zip(revenue, net_income):
            if rev != 0 and ni != 0:
                opm.append(round(((ni / rev) * 100), 2))
            else:
                opm.append(0)
        return opm
    
    def roe(self, net_income, shareholder_equity):
        roe = []
        for ni, sh_qr in zip(net_income, shareholder_equity):
            if ni != 0 and sh_qr != 0:
                roe.append(round(((ni / sh_qr) * 100), 2))
            else:
                roe.append(0)
        return roe

    def pe(self, eps):
        dates = self.yf_api_fetch.income_stmt.columns
        dates = [date.strftime('%Y-%m-%d') for date in dates][::-1]
        
        shareprice_arr = [self.get_nearest_shareprice(shareprice) for shareprice in dates]
        pe = []
        for shares, price in zip(shareprice_arr, eps):
            if price != 0:
                pe.append(shares / price)
            else:
                pe.append(0)
        return pe

    def yfinance_data(self):
        company_info = self.company_info
        def helper(key):
            if key in company_info:
                return company_info[key]
            else:
                return 0
        
        income = self.yf_api_fetch.income_stmt
        balence = self.yf_api_fetch.balance_sheet
        cashflow = self.yf_api_fetch.cash_flow
        years = [date.strftime('%Y') for date in income.columns][::-1]
        years_length = len(years)

        def finance_data_helper(key, df, length):
            if key in df.index:
                return [data if not pd.isna(data) else 0 for data in df.loc[key]][::-1]
            else:
                return [1] * length

        # =================== extracting required data from income ==================================
        revenue = finance_data_helper('Total Revenue', income, years_length)
        operating_expence = finance_data_helper('Operating Expense', income, years_length)
        net_income = finance_data_helper('Net Income', income, years_length)
        eps = finance_data_helper('Basic EPS', income, years_length)

        # ================== extracting required data from balence =================================
        total_debt = finance_data_helper('Total Debt', balence, years_length)
        shareholders_equity = finance_data_helper('Stockholders Equity', balence, years_length)
        total_assets = finance_data_helper('Total Assets', balence, years_length)
        total_liabilities = finance_data_helper('Total Liabilities Net Minority Interest', balence, years_length)
        cash_equivalents = finance_data_helper('Cash And Cash Equivalents', balence, years_length)


        # ================== extracting required data from cashflow =================================
        free_cashflow = finance_data_helper('Free Cash Flow', cashflow, years_length)
        operating_cashflow = finance_data_helper('Operating Cash Flow', cashflow, years_length)
        financing_cashflow = finance_data_helper('Financing Cash Flow', cashflow, years_length)
        investing_cashflow = finance_data_helper('Investing Cash Flow', cashflow, years_length)

        profit_margin = self.opm(revenue, net_income)
        
        roe = self.roe(net_income, shareholders_equity)

        holding = self.holding()
        data = {
            'dates' : years,
            'revenue' : revenue,
            'operating_expence' : operating_expence,
            'net_income' : net_income,
            'eps' : eps,
            'pe' : round(helper('trailingPE'), 2),
            'profit_margin' : profit_margin,
            'total_debt' : total_debt,
            'shareholders_equity' : shareholders_equity,
            'total_assets' : total_assets,
            'total_liabilities' : total_liabilities,
            'cash_equivalents': cash_equivalents,
            'roe' : roe,
            'free_cashflow' : free_cashflow,
            'operating_cashflow' : operating_cashflow,
            'investing_cashflow' : investing_cashflow,
            'financing_cashflow' : financing_cashflow,
            'holding' : holding
        }
        return data
    
    # need to work on it where we can use feature excepecially eps_trend
    def estimation(self):
        msft = self.yf_api_fetch

        d1 = msft.analyst_price_targets
        growth_estimation = msft.earnings_estimate
        d3 = msft.revenue_estimate
        d4 = msft.earnings_history
        d5 = msft.eps_trend
        d7 = msft.growth_estimates
        d8 = msft.isin
        d9 = msft.options
        d10 = msft.news
        return d10

    # Holding patterns for the institution and promotor
    def holding(self):
        # mutual_fund = self.yf_api_fetch.mutualfund_holders          #shows all mutual funds
        # institution = self.yf_api_fetch.institutional_holders
        major_holders = self.yf_api_fetch.major_holders

        insider = round(major_holders.loc['insidersPercentHeld', 'Value'] * 100, 2)
        instituation = round(major_holders.loc['institutionsPercentHeld', 'Value']*100, 2)
        public = round(100 - (insider + instituation), 2)
        return [insider, instituation, public]
    
class tradingview:
    def __init__(self, symbol) -> None:
        self.c_symbol = symbol
        self.tv_fetch_data = self.tradingview_connect()
        

    def tradingview_connect(self):
        handler = TA_Handler(
            symbol=self.c_symbol,
            screener="india",
            exchange="NSE",
            interval='1d'
        )
        analysis = handler.get_analysis()
        summary = analysis.summary
        oscillator  = analysis.oscillators
        indicators = analysis.indicators

        data = {
            "summery": summary,
            "oscillator": oscillator,
            "indicators": indicators
        }
        return data       

    def tradingview_data(self):
        def check(indicator):
            if indicator in tv_indicater_data['oscillator']['COMPUTE']:
                return tv_indicater_data['oscillator']['COMPUTE'][indicator]
            else:
                return 'NEUTRAL'
                
        yf_connect = yfinance(self.c_symbol)
        yf_data = yf_connect.company_info
        tv_indicater_data = self.tv_fetch_data
        data = {
            'line_data' : {
                '52week_high' : yf_data['fiftyTwoWeekHigh'],
                '52week_low' : yf_data['fiftyTwoWeekLow'],
                'support1': round(tv_indicater_data['indicators']['Pivot.M.Classic.S1'], 2),
                'support2': round(tv_indicater_data['indicators']['Pivot.M.Classic.S2'], 2),
                'support3': round(tv_indicater_data['indicators']['Pivot.M.Classic.S3'], 2),
                'resistance1': round(tv_indicater_data['indicators']['Pivot.M.Classic.R1'], 2),
                'resistance2': round(tv_indicater_data['indicators']['Pivot.M.Classic.R2'], 2),
                'resistance3': round(tv_indicater_data['indicators']['Pivot.M.Classic.R3'], 2)
            },
            'indicator_data' : {
            'summary': tv_indicater_data['oscillator']['RECOMMENDATION'],
            'rsi': check('RSI'),
            'adx': check('ADX'),
            'momentum': check('Mom'),
            'macd': check('MACD'),
            'bbp': check('BBP')
            }
        }
        return data


if __name__ == "__main__":
    # Example usage
    company_symbol = 'HDFCBANK'                     #RELIANCE
    data = tradingview(company_symbol)   
    tv_data = data.tradingview_data()
    print(tv_data)
    # print("=================== income ========================")
    # print(income_stmt['dates'])
    # print("revenue : ", income_stmt['revenue'])
    # print("operating_expence : ", income_stmt['operating_expence'])
    # print("net_income : ", income_stmt['net_income'])
    # print("eps : ", income_stmt['eps'])
    # print("profit_margin : ", income_stmt['profit_margin'])
    # print("total_debt : ", income_stmt['total_debt'])
    # print("shareholders_equity : ", income_stmt['shareholders_equity'])
    # print("total_assets : ", income_stmt['total_assets'])
    # print("total_liabilities : ", income_stmt['total_liabilities'])
    # print("roe : " , income_stmt['roe'])
    # print("free_cashflow : " , income_stmt['free_cashflow'])
    # print("operating_cashflow : " , income_stmt['operating_cashflow'])
    # print("financing_cashflow : " , income_stmt['financing_cashflow'])
    # print("investing_cashflow : " , income_stmt['investing_cashflow'])
    # print("cash_equivalents : " , income_stmt['cash_equivalents'])
    # print()