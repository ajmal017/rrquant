import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

##### K NEAREST NEIGHBOURS CLASSIFICATION #####
def get_data(symbol):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period="10y")
    df = df[['Open', 'High', 'Low','Close']]
    df = df.dropna()
    df['Open-Close']= df.Open - df.Close
    df['High-Low']  = df.High - df.Low
    df = df.dropna()
    return df

def knn_variables(df):
    X = df[['Open-Close', 'High-Low']]
    Y = np.where(df['Close'].shift(-1)>df['Close'],1,-1)
    return X, Y

def data_split(df, Var, split_percentage = 0.7):
    split = int(split_percentage*len(df))
    train = Var[:split]
    test = Var[split:]
    return train, test

def knn_model(k):
    return KNeighborsClassifier(n_neighbors=k)

def knn_accuracy(model_fit, X_train, Y_train, X_test, Y_test):
    accuracy_train = accuracy_score(Y_train, model_fit.predict(X_train))
    accuracy_test = accuracy_score(Y_test, model_fit.predict(X_test))
    print ('Train_data Accuracy: %.2f' % accuracy_train)
    print ('Test_data Accuracy: %.2f' % accuracy_test)
    return accuracy_train, accuracy_test

def knn_returns(knn, df, X, split_percentage = 0.7):
    split = int(split_percentage*len(df))
    df['Predicted Signal'] = knn.predict(X)
    df['Stock Returns'] = np.log(df['Close']/df['Close'].shift(1))
    df['Strategy Returns'] = df['Stock Returns']* df['Predicted Signal'].shift(1)
    cumulative_stock_rets = df[split:]['Stock Returns'].cumsum()*100
    cumulative_strat_rets = df[split:]['Strategy Returns'].cumsum()*100
    return cumulative_stock_rets, cumulative_strat_rets

def sharpe_ratio(cumulative_strat_rets, cumulative_stock_rets):
    std_dev = cumulative_strat_rets.std()
    Sharpe = ((cumulative_strat_rets-cumulative_stock_rets)/std_dev).mean()
    print ('Sharpe ratio: %.2f' % Sharpe)
    return Sharpe

def knn_plot(cumulative_stock_rets, cumulative_strat_rets):
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(cumulative_stock_rets, color='r',label = 'Stock Returns')
    ax.plot(cumulative_strat_rets, color='g', label = 'KNN Strategy Returns')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return (%)')
    plt.grid()
    plt.legend()
    plt.show()

if __name__ == "__main__":
    stock_data = get_data('AAPL')
    X, Y = knn_variables(stock_data)
    X_train, X_test = data_split(stock_data,X, 0.5)
    Y_train, Y_test = data_split(stock_data,Y, 0.5)
    knn = knn_model(5)
    model_fit = knn.fit(X_train, Y_train)
    accuracy_train, accuracy_test = knn_accuracy(model_fit, X_train, Y_train, X_test, Y_test)
    cumulative_stock_rets, cumulative_strat_rets = knn_returns(knn, stock_data, X, 0.5)
    sharpe = sharpe_ratio(cumulative_strat_rets, cumulative_stock_rets)
    knn_plot(cumulative_stock_rets, cumulative_strat_rets)