import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
%matplotlib inline
from statsmodels.graphics.gofplots import qqplot
import statsmodels.api as sm
from scipy.stats import shapiro, anderson, normaltest
from pandas_datareader import data as pdr
import yfinance as yf
import re
import warnings

yf.pdr_override()
warnings.filterwarnings("ignore")

def asx_200():
    return pd.read_csv('~/data/ASX200LIST.csv').sort_values('Market Cap', ascending = False).reset_index().drop(columns = ['index'])

def sectors(asx_list = asx_200()):
    sector_breakdown = pd.DataFrame(asx_list['Sector'].value_counts())
    sector_breakdown['Proportion'] = sector_breakdown['Sector']/sum(sector_breakdown['Sector'])
    sector_breakdown = sector_breakdown.reset_index().rename(columns = {'index':'Sector','Sector':'Count','Proportion':'Proportion'})
    return sector_breakdown

def ticks(symbollist):
    i = 1
    symbols = symbollist[0]
    while i < len(symbollist):
        symbols += ' '+ symbollist[i]
        i += 1
    return yf.Tickers(symbols).tickers

def stocklist(symbollist):
    tick_objects = list(ticks(symbollist))
    rdates = []
    roptions = []
    for t in range(len(tick_objects)):
        try:
            rdates.append(tick_objects[t].calendar.loc['Earnings Date'].Value.strftime('%d/%m/%Y'))
            option_series = pd.DataFrame(tick_objects[t].options).rename(columns = {0:'Expiry'})
            options_after_report = option_series.loc[option_series['Expiry'] > rdates[t]]
            roptions.append(options_after_report.iloc[0,0])
        except:
            rdates.append('NA')
            roptions.append(tick_objects[t].options[0])
    stocks = pd.DataFrame({'Symbol':symbollist,'Ticker Object':tick_objects,'Earnings Date':rdates, 'Option Expiry':roptions})
    return stocks

def option_straddles(symbol):
    stock = yf.Ticker(symbol)
    calls, puts = stock.option_chain(stock.options[0])
    std_close = stock.history().Close.head(21).std().round()
    upper_strike = stock.history().iloc[0,3].round() + (0.5*std_close)
    lower_strike = stock.history().iloc[0,3].round() - (0.5*std_close)
    call_strikes = calls.loc[(calls['strike'] <= upper_strike) & (calls['strike'] >= lower_strike)]['strike']
    put_strikes = puts.loc[(puts['strike'] <= upper_strike) & (puts['strike'] >= lower_strike)]['strike']
    strikes = call_strikes[call_strikes.isin(put_strikes)]#.reset_index().drop(columns = ['index'])
    call_legs = calls.loc[calls['strike'].isin(strikes)]
    put_legs = puts.loc[puts['strike'].isin(strikes)]
    call_legs['Type'] = 'CALL'
    put_legs['Type'] = 'PUT'
    drop_cols = ['change','percentChange','index','inTheMoney','contractSize','currency']
    straddle_contracts = pd.concat([call_legs,put_legs]).reset_index().drop(columns = drop_cols)
    straddle_contracts['mid'] = (straddle_contracts['ask'] + straddle_contracts['bid'])/2
    straddle_contracts['Percent Cost'] = straddle_contracts['mid']/straddle_contracts['strike']
    straddle_contracts['Upper Breakeven'] = straddle_contracts['strike']*(1+straddle_contracts['Percent Cost'])
    straddle_contracts['Lower Breakeven'] = straddle_contracts['strike']*(1-straddle_contracts['Percent Cost'])
    straddle_contracts['Last Price % Cost'] = (straddle_contracts['lastPrice']/straddle_contracts['strike']).round(4)
    cols = ['Type','strike','bid','ask','mid','Percent Cost','Upper Breakeven','Lower Breakeven','lastPrice','Last Price % Cost',
            'lastTradeDate','openInterest','volume','impliedVolatility','contractSymbol']
    straddle_contracts = straddle_contracts[cols].sort_values(['strike','Type']).reset_index().drop(columns = ['index'])
    straddle_contracts = straddle_contracts.rename(columns = {'strike':'Strike','bid':'Bid','ask':'Ask','mid':'Mid','lastPrice':'Last Price',
                                         'lastTradeDate':'Last Traded','openInterest':'Open Interest',
                                         'volume':'Volume','impliedVolatility':'Impl. Vol','contractSymbol':'Contract'})
    for i in range(len(straddle_contracts['Last Traded'])):
        straddle_contracts.loc[i,'Last Traded'] = straddle_contracts.loc[i,'Last Traded'].strftime('%H:%M %d/%m/%Y')
    return straddle_contracts

def all_straddles(symbollist):
    map_ticks = map(option_straddles, ticks(symbollist))
    mapped_df = pd.DataFrame(map_ticks)
    mapped_df['Symbols'] = symbollist
    mapped_df = mapped_df.set_index('Symbols')
    return mapped_df

def get_ydata(symbollist, startdate = dt.datetime(2008, 12, 1), enddate =  dt.datetime.now()):
    def ydata(tick):
        return (pdr.get_data_yahoo(tick, start=startdate, end=enddate))
    tickers = ticks(symbollist)
    datas = map (ydata, tickers)
    return(pd.concat(datas, keys=tickers, names=['Ticker', 'Date']))

def historic_price(symbol):
    tick = yf.Ticker(symbol).ticker
    price_data = tick.history(start = '2008-12-01').drop(columns = ['Dividends','Stock Splits'])
    return price_data

def isolate_stock(symbol, all_data):
    stock_data = all_data.iloc[all_data.index.get_level_values('Ticker') == symbol]
    stock_data.index = stock_data.index.droplevel('Ticker')
    return stock_data

def concat_returns(stock_returns_list, symbollist):
    return_data = pd.concat(stock_returns_list, axis=1)[1:]
    return_data.columns = symbollist
    return return_data

def stock_analysis(stock_data):
    stock['Returns'] = np.log(stock['Adj Close']/stock['Adj Close'].shift(1))
    stock["5-Day SMA"] = np.array(stock['Adj Close'].rolling(5).mean())
    stock["20-Day SMA"] = np.array(stock['Adj Close'].rolling(20).mean())
    stock["5-Day HV (%)"] = np.array(stock['Adj Close'].rolling(5).std())
    stock["20-Day HV (%)"] = np.array(stock['Adj Close'].rolling(20).std())
    stock.fillna(0, inplace=True)#.dropna()
    return stock

def log_returns(stock_data):
    daily_log_returns = np.log(stock_data['Adj Close']/stock_data['Adj Close'].shift(1))
    daily_log_returns.fillna(0, inplace=True)
    return daily_log_returns

def qqplot_returns(returns):
    qqplot(returns, line='s')
    plt.title('Daily Returns QQ Plot')
    plt.show()

def get_sample(data, sample_proportion = 0.25, seed = 1111):
    sampled_data = data.sample(frac = sample_proportion, random_state=seed)
    return sampled_data

def z_scores(returns):
    z = ((returns-np.mean(returns))/np.std(returns)).fillna(0, inplace=True)
    return z

def returns_hist(all_data):
    daily_close_px = all_data[['Adj Close']].reset_index().pivot('Date', 'Ticker', 'Adj Close')
    daily_pct_change = daily_close_px.pct_change()
    daily_pct_change.hist(bins=50, sharex = True, align = 'mid',figsize=(15, 10))
    plt.show()

def cumrets_plot(all_data):
    daily_close_px = all_data[['Adj Close']].reset_index().pivot('Date', 'Ticker', 'Adj Close')
    daily_pct_change = daily_close_px.pct_change()
    cum_daily_return = (1 + daily_pct_change).cumprod()
    cum_daily_return.plot(figsize=(15, 10))
    plt.title('Cumulative Daily Log Returns')
    plt.ylabel('Returns (%)')
    plt.show()

def vol_plot(all_data, min_periods = 200):
    daily_close_px = all_data[['Adj Close']].reset_index().pivot('Date', 'Ticker', 'Adj Close')
    daily_pct_change = daily_close_px.pct_change()
    vol = daily_pct_change.rolling(min_periods).std() * np.sqrt(min_periods)
    vol.plot(figsize=(16, 9))
    plt.ylabel('Volatility (%)')
    plt.title(str(min_periods) +" Day Moving Historical Volatility")
    plt.show()

def normality_tests(returns):
    stat_s, p_s = shapiro(returns)
    print('Shapiro Statistic = %.3f, P-Value = %.3f' % (stat_s, p_s))
    alpha_s = 0.05
    if p_s > alpha_s:
        print('P-Value > Alpha: Do Not Reject H0 - Data is from a Normal Distribution @ Significance Level = %.2f\n' % alpha_s)
    else:
        print('P-Value < Alpha: Reject H0 - Data is not from a Normal Distribution @  Significance Level = %.2f \n' % alpha_s)


    stat_d, p_d = normaltest(returns)
    print("D'Agostino Statistic = %.3f, P-Value = %.3f" % (stat_d, p_d))
    alpha_d = 0.05
    if p_d > alpha_d:
        print('P-Value > Alpha: Do Not Reject H0 - Data is from a Normal Distribution @ Significance Level = %.2f\n' % alpha_d)
    else:
        print('P-Value < Alpha: Reject H0 - Data is not from a Normal Distribution @  Significance Level = %.2f \n' % alpha_d)

    result = anderson(returns, dist = 'norm')
    print('Anderson-Darling Statistic = %.3f' % result.statistic)
    for i in range(len(result.critical_values)):
        print('Critical Value = %.3f @ Alpha = %.3f ' % (result.critical_values[i],result.significance_level[i]/100))
        if result.statistic < result.critical_values[i]:
            print('Statistic < CV: Do not Reject H0 - Data is from a Normal Distribution @ Significance Level = %.3f \n' % (result.significance_level[i]/100))
        else:
            print('Statistic > CV: Reject H0 - Data is not from a Normal Distribution @ Significance Level %.3f \n' % (result.significance_level[i]/100))

#Ordinary Least Squares Regression
def ols_reg(constant_returns, response_returns):
    X = sm.add_constant(constant_returns)
    model = sm.OLS(response_returns,X).fit()
    residuals = model.resid
    print(model.summary())
    fig = sm.qqplot(residuals, line = 's')
    plt.show()

def fff3_data():
    fff3 = pd.read_csv("~/data/F-F_Research_Data_Factors_daily.csv").dropna()
    fff3.Date = pd.to_datetime(fff3.Date)
    fff3 = fff3.loc[fff3.Date >= '2008-12-01'].reset_index().drop(columns = ['index'])
    fff3 = fff3.set_index('Date')
    return fff3

if __name__ == "__main__":
    symbollist = list(asx_200()['Symbol'])
    asx_tickers = ticks(symbollist)
    print(asx_tickers)
    all_data = get_ydata(asx_tickers)
    all_returns = log_returns(all_data)
    returns_hist(all_data)
    cumrets_plot(all_data)
    vol_plot(all_data)

    stock_data = isolate_stock(asx_tickers[0],all_data)
    returns = log_returns(stock_data)
    qqplot_returns(returns)
    normality_tests(returns)
    constant = isolate_stock('RIO',all_returns)
    response = isolate_stock('BHP',all_returns)
    ols_reg(constant, response)

    us_symbollist = ['AAPL','GOOG','MSFT']
    us_tickers = ticks(us_symbollist)
    print(stocklist(us_symbollsit))
    aapl_straddles = option_straddles(us_symbollist[0])
    top3_straddles = all_straddles(us_symbollist)
