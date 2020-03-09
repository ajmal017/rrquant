#Win Rate MM
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import talib
import seaborn as sns

def stock(symbol):
    df = yf.Ticker(symbol).history(period = '10y').drop(columns = ['Volume','Dividends','Stock Splits'])
    df['MA_30'] = df['Close'].rolling(10).mean()
    df['Pos'] = np.where(df['Close'] > df['MA_30'],1,-1)
    df['Pct_Chg'] = df.Close.pct_change()
    df = df.dropna()
    return df

def stock_fixed_ratio(symbol,BASE_QTY):
    df = yf.Ticker(symbol).history(period = '10y').drop(columns = ['Volume','Dividends','Stock Splits'])
    df['MA'] = df['Close'].rolling(window=15).mean()
    df['Pct_Chg'] = df.Close.pct_change()
    df['Pos'] = np.where(df['MA'] < df['Close'],1,-1)
    df = df.dropna()
    df['PNL'] = df['Pos'] * df.Pct_Chg #* df['qty']
    df['PNL_$'] = (df['PNL'] * BASE_QTY*df['Close']).cumsum()
    df['qty'] = .5 * (np.sqrt(1 + 8*(df['PNL_$']/BASE_QTY)) + 1)
    df['PNL_wt'] = df['PNL'] * df['qty']
    df['wt_total'] = df['PNL_wt'].cumsum()
    df['reg_total'] = df['PNL'].cumsum()
    df = df.reset_index()
    return df

def get_rets(df,qty):
    df['Return'] = ((df['Pct_Chg'] ) * df['Pos'] * qty)
    df['Cum_ret'] = df['Return'].cumsum()
    return df

def win_rate_MM(df):
    df['LWC'] = np.where((df['Pos'] > 0) & (df['Pct_Chg'] > 0),1,0).cumsum()
    df['SWC'] = np.where((df['Pos'] < 0) & (df['Pct_Chg'] < 0),1,0).cumsum()
    long_ct = df[df['Pos'] > 0].shape[0]
    short_ct = df.shape[0] - long_ct
    df['LWP'] = df['LWC'] / long_ct
    df['SWP'] = df['SWC'] / short_ct
    return df

def get_weighted_rets(df,qty):
    p_ret = df['Pct_Chg'] * df['Pct_Chg'] * qty * df['LWP']
    n_ret = df['Pct_Chg'] * df['Pct_Chg'] * qty * df['SWP']
    df['Return'] = np.where(df['Pos'] > 0,p_ret,n_ret)
    df['Cum_ret'] = df['Return'].cumsum()
    return df

def get_fixed_ratio(P,D):
    qty = .5 * (np.sqrt(1 + 8*(P/D)) + 1)
    return qty

if __name__ == "__main__":
    aapl = stock('AAPL')
    rets = get_rets(aapl,100)
    plt.style.use('seaborn')
    rets.plot(y='Cum_ret',figsize=(18,10),title='Cumulative Returns (%)')
    plt.ylabel('Return (%)')
    plt.xlabel('Date')
    plt.show()

    aapl_wr = win_rate_MM(rets)
    wt_ret = get_weighted_rets(aapl_wr,100)
    rets.plot(y='Cum_ret',figsize=(18,10),title='Cumulative Weighted Returns (%)')
    plt.ylabel('Return (%)')
    plt.xlabel('Date')
    plt.show()

    #Fixed Ratio: get a MM system that performs better
    aapl_fr = stock_fixed_ratio('AAPL', 1000)
    aapl_fr.plot(x='Date', y=['wt_total', 'reg_total'],title = 'Fixed Ratio Cumulative Returns', figsize=(18,10), grid=True,cmap='cividis')
    plt.ylabel('Return (%)')
    plt.xlabel('Date')
    plt.show()
