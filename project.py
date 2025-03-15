import pandas as pd
from analysis import analysis

if __name__ == '__main__':
    c_name = 'ITC'
    details = analysis(c_name)

    df = pd.DataFrame(details.share_price_range('1mo', '1d'))
    print(df)