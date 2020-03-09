
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
import scipy.stats as scs
from scipy.stats import norm
import yfinance as yf
from tabulate import tabulate

def value_at_risk(symbol):
    df = yf.Ticker(symbol).history(period = '10y')
    df = df[['Close']]
    df['returns'] = df.Close.pct_change()
    mean = np.mean(df['returns'])
    std_dev = np.std(df['returns'])
    df['returns'].hist(bins=40, density=True, histtype='stepfilled', alpha=0.5)
    x = np.linspace(mean - 3*std_dev, mean + 3*std_dev, 100)
    plt.plot(x,scs.norm.pdf(x, mean, std_dev),"r")
    plt.show()
    VaR_90 = norm.ppf(1-0.9, mean, std_dev)
    VaR_95 = norm.ppf(1-0.95, mean, std_dev)
    VaR_99 = norm.ppf(1-0.99, mean, std_dev)
    print(tabulate([['90%', VaR_90], ['95%', VaR_95], ["99%", VaR_99]], headers=['Confidence Level', 'Value at Risk']))

def value_at_risk2(symbol):
    df = yf.Ticker(symbol).history(period = '10y')
    df = df[['Close']]
    df['returns'] = df.Close.pct_change()
    df = df.dropna()
    plt.hist(df.returns, bins=40)
    plt.xlabel('Returns')
    df.sort_values('returns', inplace= True, ascending = True)
    plt.ylabel('Fequency')
    plt.grid(True)
    plt.show()
    df.sort_values('returns', inplace= True, ascending = True)
    VaR_90= df['returns'].quantile(0.1)
    VaR_95= df['returns'].quantile(0.05)
    VaR_99= df['returns'].quantile(0.01)
    print(tabulate([['90%', VaR_90], ['95%', VaR_95], ["99%", VaR_99]], headers=['Confidence Level', 'Value at Risk']))

if __name__ == "__main__":
    value_at_risk('AAPL')
    value_at_risk2('AAPL')
