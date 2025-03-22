from datetime import date, datetime, timedelta
import numpy as np
import yfinance as yf
from tradingview_ta import TA_Handler, Interval
import pandas as pd
import requests


class CompanyDetails:
    def __init__(self, name):
        self.company_name = f'{name}.NS'
        self.yf_api_fetch = yf.Ticker(self.company_name)
        self.company_info = self.yf_api_fetch.info
        self.company_symbol = name
        self.tv_fetch_data = self.tradingviewConnect()


    def tradingviewConnect(self):
        handler = TA_Handler(
            symbol=self.company_symbol,
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


    def sharePrice(self):
        data = self.company_info
        if 'currentPrice' in data:
            return data['currentPrice']
        else:
            return None
        
    def sharePriceRange_test(self, period='max', interval='1d'):
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
                'close': share_price,
                'volume': volume
            })
        return filtered_data

    def sharePriceRange(self, period='max', interval='1d'):
        stock = self.yf_api_fetch
        share_price_arr = stock.history(period=period, interval=interval)
        if share_price_arr.empty : return []
        filtered_data = []    
        for index, row in share_price_arr.iterrows():
            date = index.strftime('%Y-%m-%d')
            share_price = round(row['Close'], 2)
            filtered_data.append({
                'Date' : date,
                'Close' : share_price
            })
        return filtered_data

    def getNearSharePrice(self, date):
        date = datetime.strptime(date, '%Y-%m-%d').date()
        start_date = (date - timedelta(days=5)).strftime('%Y-%m-%d')  # start 10 days before the date
        end_date = (date + timedelta(days=5)).strftime('%Y-%m-%d')
        shareprice = self.yf_api_fetch.history(start=start_date, end=end_date)
        return round((shareprice['Close'].iloc[0]), 2)

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
        
        shareprice_arr = [self.getNearSharePrice(shareprice) for shareprice in dates]
        pe = []
        for shares, price in zip(shareprice_arr, eps):
            if price != 0:
                pe.append(shares / price)
            else:
                pe.append(0)
        return pe
    
    def getRevenueIncome(self):
        income = self.yf_api_fetch.income_stmt
        years = [date.strftime('%Y') for date in income.columns][::-1]
        years_length = len(years)
        
        def finance_data_helper(key, df, length):
            if key in df.index:
                return [data if not pd.isna(data) else 0 for data in df.loc[key]][::-1]
            else:
                return [1] * length
    
        def val_to_crore(arr):
            return [round(val / 10000000, 2) for val in arr]

        revenue = finance_data_helper('Total Revenue', income, years_length)
        net_income = finance_data_helper('Net Income', income, years_length)
        if revenue[0] == 0:
                years = years[1:]
                revenue = revenue[1:]
                net_income = net_income[1:]

        data = {
            'years' : [int(year) for year in years],
            'revenue' : val_to_crore(revenue),
            'income' : val_to_crore(net_income)
        }
    
        return data
    

    def companyDetails(self):
        company_info = self.company_info
        income = self.yf_api_fetch.income_stmt
        balence = self.yf_api_fetch.balance_sheet
        cashflow = self.yf_api_fetch.cash_flow
        years = [date.strftime('%Y') for date in income.columns][::-1]
        years_length = len(years)
        tv_indicater_data = self.tv_fetch_data
        
        def helper(key):
            if key in company_info:
                return company_info[key]
            else:
                return 0
        
        def finance_data_helper(key, df, length):
            if key in df.index:
                return [data if not pd.isna(data) else 0 for data in df.loc[key]][::-1]
            else:
                return [1] * length
        
        def check(indicator):
            if indicator in tv_indicater_data['oscillator']['COMPUTE']:
                return tv_indicater_data['oscillator']['COMPUTE'][indicator]
            else:
                return 'NEUTRAL'
            
        def val_to_crore(arr):
            return [round(val / 10000000, 2) for val in arr]

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

        if revenue[0] == 0:
            years = years[1:]
            revenue = revenue[1:]
            net_income = net_income[1:]
            eps = eps[1:]
            roe = roe[1:]
            operating_expence = operating_expence[1:]
            profit_margin = profit_margin[1:]
            shareholders_equity = shareholders_equity[1:]
            total_assets = total_assets[1:]
            total_liabilities = total_liabilities[1:]
            cash_equivalents = cash_equivalents[1:]
            free_cashflow = free_cashflow[1:]
            operating_cashflow = operating_cashflow[1:]
            investing_cashflow = investing_cashflow[1:]
            financing_cashflow = financing_cashflow[1:]


        data = {
            'years' : [int(year) for year in years],
            'revenue' : val_to_crore(revenue),
            'income' : val_to_crore(net_income),
            'eps' : eps,
            'roe' : roe,
            'operating_expence' : val_to_crore(operating_expence),
            'profit_margin' : profit_margin,
            'shareholders_equity' : val_to_crore(shareholders_equity),
            'outstanding_shares' : round((helper('sharesOutstanding')/10000000), 2),
            'line_data' : {
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
    

    def companyDetails_test(self):
        company_info = self.company_info
        income = self.yf_api_fetch.income_stmt
        balence = self.yf_api_fetch.balance_sheet
        cashflow = self.yf_api_fetch.cash_flow
        years = [date.strftime('%Y') for date in income.columns][::-1]
        years_length = len(years)
        tv_indicater_data = self.tv_fetch_data
        
        def helper(key):
            if key in company_info:
                return company_info[key]
            else:
                return 0
        
        def finance_data_helper(key, df, length):
            if key in df.index:
                return [data if not pd.isna(data) else 0 for data in df.loc[key]][::-1]
            else:
                return [1] * length
        
        def check(indicator):
            if indicator in tv_indicater_data['oscillator']['COMPUTE']:
                return tv_indicater_data['oscillator']['COMPUTE'][indicator]
            else:
                return 'NEUTRAL'
            
        def val_to_crore(arr):
            return [round(val / 10000000, 2) for val in arr]

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

        if revenue[0] == 0:
            years = years[1:]
            revenue = revenue[1:]
            net_income = net_income[1:]
            eps = eps[1:]
            roe = roe[1:]
            operating_expence = operating_expence[1:]
            profit_margin = profit_margin[1:]
            shareholders_equity = shareholders_equity[1:]
            total_assets = total_assets[1:]
            total_liabilities = total_liabilities[1:]
            cash_equivalents = cash_equivalents[1:]
            free_cashflow = free_cashflow[1:]
            operating_cashflow = operating_cashflow[1:]
            investing_cashflow = investing_cashflow[1:]
            financing_cashflow = financing_cashflow[1:]


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
            'years' : [int(year) for year in years],
            'revenue' : val_to_crore(revenue),
            'operating_expence' : val_to_crore(operating_expence),
            'income' : val_to_crore(net_income),
            'eps' : eps,
            'pe' : round(helper('trailingPE'), 2),
            'pb' : round(helper('priceToBook'), 2),
            'profit_margin' : profit_margin,
            'total_debt' : total_debt,
            'shareholders_equity' : val_to_crore(shareholders_equity),
            'total_assets' : val_to_crore(total_assets),
            'total_liabilities' : val_to_crore(total_liabilities),
            'cash_equivalents': val_to_crore(cash_equivalents),
            'roe' : roe,
            'free_cashflow' : val_to_crore(free_cashflow),
            'operating_cashflow' : val_to_crore(operating_cashflow),
            'investing_cashflow' : val_to_crore(investing_cashflow),
            'financing_cashflow' : val_to_crore(financing_cashflow),
            'holding' : holding,
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
            'line_data' : {
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
    

    # Holding patterns for the institution and promotor
    def holding(self):
        # mutual_fund = self.yf_api_fetch.mutualfund_holders          #shows all mutual funds
        # institution = self.yf_api_fetch.institutional_holders
        major_holders = self.yf_api_fetch.major_holders

        insider = round(major_holders.loc['insidersPercentHeld', 'Value'] * 100, 2)
        instituation = round(major_holders.loc['institutionsPercentHeld', 'Value']*100, 2)
        public = round(100 - (insider + instituation), 2)
        return [insider, instituation, public]
