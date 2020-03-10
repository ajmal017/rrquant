import numpy as np
import matplotlib.pyplot as plt
import seaborn
import pandas as pd
import datetime
import mibian
seaborn.set(style="darkgrid")

# List of Option Strategies & Descriptions

def strategy_description():
    strats_dict = {"stock_payoff": ' ',
    "short_stock_payoff": ' ',
    "call_payoff": ' ',
    "short_call_payoff": ' ',
    "put_payoff": ' ',
    "short_put_payoff": ' ',
    "synthetic_call_payoff": ' ',
    "synthetic_put_payoff": ' ',
    "covered_call_payoff": ' ',
    "protective_put_payoff": ' ',
    "bull_call_spread_payoff":'A bull call spread is purchasing a call option, and simultaneously selling another call option (on the same underlying asset) with the same expiration date but a higher strike price. Since this is a debit spread, the maximum loss is restricted to the net premium paid for the position, while the maximum profit is equal to the difference in the strike prices of the calls less the net premium paid to put on the position.',
    "bear_call_spread_payoff":'A bear call spread is selling a call option, and simultaneously purchasing another call option with the same expiration date but at a higher strike price. Since this is a credit spread, the maximum gain is restricted to the net premium received for the position, while the maximum loss is equal to the difference in the strike prices of the calls less the net premium received.',
    "bull_put_spread_payoff":'A bull put spread is writing a put option, and simultaneously purchasing another put option with the same expiration date but a lower strike price. Since this is a credit spread, the maximum gain is restricted to the net premium received for the position, while the maximum loss is equal to the difference in the strike prices of the puts less the net premium received.',
    "bear_put_spread_payoff":'A bear put spread is purchasing a put option, and simultaneously selling another put option with the same expiration date but a lower strike price. Since this is a debit spread, the maximum loss is restricted to the net premium paid for the position, while the maximum profit is equal to the difference in the strike prices of the puts less the net premium paid to put on the position.',
    "bear_call_ladder": 'A Bear Call Ladder that allows earning profits till the underlying price reaches a desired strike price. It resets during specific trade levels by capping the profit between the old strike and the new strike price in either or both directions, thus allowing flexibility in the payoff. Like the rungs of a ladder, the trigger strikes reduce risk and once the market price of the asset reaches the trigger, it locks in the profit, thus increasing the profitability.It mainly protects the downside of a Call sold by insuring it i.e. by buying a Call of a higher strike price. This strategy is successfule when it is speculated that the market would be moving significantly higher.',
    "long_combo_payoff": 'A Long Combo Spread is a bullish strategy and involves shorting a OTM Lower Strike Put and buying a OTM High Strike Call.',
    "collar_payoff": 'A Protective Collar is a Covered Call position, with an additional Protective Put to "collar" the value of a security position between 2 bounds.',
    "straddle_spread_payoff": ' ',
    "strangle_spread_payoff": ' ',
    "iron_condor_payoff": 'An Iron Condor Spread is a four-legged strategy, combining a bull put and a bear call. It is acheived through shorting an OTM higher put and an OTM lower call and taking a long position in an OTM higher strike call and OTM lower strike put.',
    "butterfly_spread_payoff": 'Butterfly Options Strategy is a combination of Bull Spread and Bear Spread, a Neutral Trading Strategy, since it has limited risk options and a limited profit potential. It is practised on the stocks whose underlying Price is expected to change very little over its lifetime.',
    "iron_butterfly_payoff": ' ',
    "jade_lizard_payoff": 'A Jade Lizard Trading Strategy is generally practised if there was a high IV and/or if the stock had recently fallen i.e the stocks are oversold. They are most beneficial when underlying stays or drifts toward the strike. High profits are produced in high IV and non-bearish environments'
    }
    strategy_df = pd.DataFrame({"Strategy":list(strats_dict.keys()),"Description":list(strats_dict.values())})
    return strategy_df


# Stock Price (s) at Future Time (T)
def s_T(min_price, max_price):
    return np.arange(min_price,max_price,1)

# Max Profit and Loss
def profit_loss(payoff):
    Profit = max(payoff).round(4)
    Loss = min(payoff).round(4)
    print('Max Profit: ' + str(Profit) + ' | Max Loss: '+ str(Loss))
    return Profit, Loss

##### Stock and Single Leg Option Payoffs #####
# Stock Payoff
def stock_payoff(sT, s0):
    return (sT - s0)

# Short Stock Payoff
def short_stock_payoff(sT, s0):
    return (sT - s0)*-1.0

# Call Payoff
def call_payoff (sT, call_strike, call_premium):
    return np.where(sT> call_strike, sT-  call_strike, 0)- call_premium

# Short Call Payoff
def short_call_payoff(sT, short_call_strike, short_call_premium):
    return call_payoff(sT, short_call_strike, short_call_premium)*-1.0

# Put Payoff
def put_payoff(sT, put_strike, put_premium):
    return np.where(sT < put_strike, put_strike - sT, 0) - put_premium

# Short Put Payoff
def short_put_payoff(sT, short_put_strike, short_put_premium):
    return put_payoff(sT, short_put_strike, short_put_premium)*-1.0

# Synthetic Call Payoff
def synthetic_call_payoff(sT, s0, put_strike, put_premium):
    put = put_payoff(sT, put_strike, put_premium)
    stock = stock_payoff(sT, s0)
    return put + stock

# Synthetic Put Payoff
def synthetic_put_payoff(sT, s0, call_strike, call_premium):
    call = call_payoff(sT, call_strike, call_premium)
    short_stock = short_stock_payoff(sT, s0)
    return call + short_stock

# Protective Put Payoff
def protective_put_payoff(sT, s0, put_strike, put_premium):
    put = put_payoff(sT, put_strike, put_premium)
    stock = stock_payoff(sT, s0)
    return put + stock

# Covered Call Payoff
def covered_call_payoff(sT, s0, short_call_strike, short_call_premium):
    short_call = short_call_payoff(sT, short_call_strike, short_call_premium)
    stock = stock_payoff(sT, s0)
    return short_call + stock


##### Two Leg Spread Payoffs #####
# Bull Call Spread Payoff
def bull_call_payoff(sT, K1_call_strike, K1_call_premium, K2_short_call_strike, K2_short_call_premium):
    K1_call = call_payoff(sT, K1_call_strike, K1_call_premium)
    K2_short_call = short_call_payoff(sT, K2_short_call_strike, K2_short_call_premium)
    return K1_call + K2_short_call

# Bear Call Spread Payoff
def bear_call_payoff(sT, K1_short_call_strike, K1_short_call_premium, K2_call_strike, K2_call_premium):
    K1_short_call = short_call_payoff(sT, K1_short_call_strike, K1_short_call_premium)
    K2_call = call_payoff(sT, K2_call_strike, K2_call_premium)
    return K1_short_call + K2_call

# Bull Put Spread Payoff
def bull_put_payoff(sT, K1_put_strike, K1_put_premium, K2_short_put_strike,  K2_short_put_premium):
    K1_put = put_payoff(sT, K1_put_strike, K1_put_premium)
    K2_short_put = short_put_payoff(sT, K2_short_put_strike, K2_short_put_premium)
    return K1_put + K2_short_put

# Bear Put Spread Payoff
def bear_put_payoff(sT, K1_short_put_strike,  K1_short_put_premium, K2_put_strike, K2_put_premium):
    K1_short_put = short_put_payoff(sT, K1_short_put_strike, K1_short_put_premium)
    K2_put = put_payoff(sT, K2_put_strike, K2_put_premium)
    return  K1_short_put + K2_put

# Collar Spread Payoff (Aka Protective Collar)
def collar_payoff(sT, K1_put_strike, K1_put_premium, K2_short_call_strike, K2_short_call_premium):
    K2_short_call = short_call_payoff(sT, K2_short_call_strike, K2_short_call_premium)
    K1_put = put_payoff(sT, K1_put_strike, K1_put_premium)
    return K1_put + K2_short_call

# Long Combo Spread Payoff (Inverted Collar Spread)
def long_combo_payoff(sT, K1_short_put_strike, K1_short_put_premium, K2_call_strike, K2_call_premium):
    K1_short_put = short_put_payoff(sT, K1_short_put_strike, K1_short_put_premium)
    K2_call = call_payoff(sT, K2_call_strike, K2_call_premium)
    return K1_short_put + K2_call

# Straddle Spread Payoff
def straddle_payoff(sT, K1_strike, K1_call_premium, K1_put_premium):
    K1_call = call_payoff(sT, K1_strike, K1_call_premium)
    K1_put = put_payoff(sT, K1_strike, K1_put_premium)
    return K1_call + K1_put

# Strangle Spread Payoff
def strangle_payoff(sT, K1_put_strike, K1_put_premium,  K2_call_strike, K2_call_premium):
    K1_put = put_payoff(sT, K1_put_strike, K1_put_premium)
    K2_call = call_payoff(sT, K2_call_strike, K2_call_premium)
    return K1_put + K2_call


##### Multi Leg Spread Payoffs #####
# Bear Call Ladder Spread Payoff
def bear_call_ladder_payoff(sT, K1_short_call_strike, K1_short_call_premium, K2_call_strike, K2_call_premium, K3_call_strike, K3_call_premium):
    K1_short_call = short_call_payoff(sT, K1_short_call_strike, K1_short_call_premium)
    K2_call = call_payoff(sT, K2_call_strike, K2_call_premium)
    K3_call = call_payoff(sT, K3_call_strike, K3_call_premium)
    return  K1_short_call + K2_call + K3_call

# Iron Condor Spread Payoff
def iron_condor_payoff(sT, K1_put_strike, K1_put_premium, K2_short_put_strike, K2_short_put_premium, K3_short_call_strike, K3_short_call_premium, K4_call_strike, K4_call_premium):
    K1_put = put_payoff(sT, K1_put_strike, K1_put_premium)
    K2_short_put = short_put_payoff(sT, K2_short_put_strike, K2_short_put_premium)
    K3_short_call = short_call_payoff(sT, K3_short_call_strike, K3_short_call_premium)
    K4_call = call_payoff(sT, K4_call_strike, K4_call_premium)
    return K1_put + K2_short_put  + K3_short_call + K4_call

# Butterfly Spread Payoff
def butterfly_payoff(sT, K1_call_strike, K1_call_premium, K2_short_call_strike, K2_short_call_premium, K3_call_strike, K3_call_premium):
    K1_call = call_payoff(sT, K1, K1_call_premium)
    K2_short_call = short_call_payoff(sT, K2, K2_short_call_premium)
    K3_call = call_payoff(sT, K3, K3_call_premium)
    return K1_call + 2*(K2_short_call) + K3_call

# Iron Butterfly Spread Payoff
def iron_butterfly_payoff(sT, K1_put_strike, K1_put_premium, K2_short_strike, K2_short_call_premium, K2_short_put_premium, K3_call_strike, K3_call_premium):
    K1_put = put_payoff(sT, K1_put_strike, K1_put_premium)
    K2_short_call = short_call_payoff(sT, K2_short_strike, K2_short_call_premium)
    K2_short_put = short_put_payoff(sT, K2_short_strike, K2_short_put_premium)
    K3_call = call_payoff(sT, K3_call_strike, K3_call_premium)
    return K1_put + K2_short_put + K2_short_call + K3_call

# Jade Lizard Spread Payoffs
def jade_lizard_payoff(sT,K1_short_put_strike, K1_short_put_premium, K2_short_call_strike, K2_short_call_premium, K3_call_strike, K3_call_premium):
    K1_short_put =  short_put_payoff(sT, K1_short_put_strike, K1_short_put_premium)
    K2_short_call = short_call_payoff(sT, K2_short_call_strike, K2_short_call_premium)
    K3_call = call_payoff(sT, K3_call_strike, call_premium)
    return K1_short_put + K2_short_call + K3_call


###### Payoff Plots #######
### Stock Payoff Plots ###
def stock_payoff_plot(sT, stock_payoff):
    fig, ax = plt.subplots()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT,stock_payoff,label='Stock Payoff',color='g')
    plt.xlabel('Stock Price')
    plt.ylabel('Profit and loss')
    plt.show()

def short_stock_payoff_plot(sT, short_stock_payoff):
    fig, ax = plt.subplots()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT,short_stock_payoff,label='Stock Payoff',color='r')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit and loss')
    plt.show()

### Call Payoff Plots ###
def call_payoff_plot(sT, call_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT,call_payoff,label='Long Call',color='g')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit and loss')
    plt.show()

def short_call_payoff_plot(sT, short_call_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT, short_call_payoff,label='Short Call',color='r')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit and loss')
    plt.show()

def covered_call_plot(sT, covered_call_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT,covered_call_payoff, color = 'b')
    ax.set_title('Covered Call Payoff')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit and loss')
    plt.show()

def synthetic_call_plot(sT, synthetic_call_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT,synthetic_call_payoff, color = 'b')
    ax.set_title('Synthetic Call Payoff')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit and loss')
    plt.show()

### Put Payoff Plots ###
def put_payoff_plot(sT, put_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT, put_payoff, color ='g')
    ax.set_title('Long Strike Put')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit & Loss')
    plt.show()

def short_put_payoff_plot(sT, short_put_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT, short_put_payoff, color ='r')
    ax.set_title('Short Strike Put')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit & Loss')
    plt.show()

def protective_put_plot(sT, protective_put_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT,protective_put_payoff, color = 'b')
    ax.set_title('Protective Put Payoff')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit and loss')
    plt.show()

def synthetic_put_payoff_plot(sT, synthetic_put_payoff):
    fig, ax = plt.subplots()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT,synthetic_put_payoff,color = 'magenta')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit and loss')
    plt.show()

### Two Leg Sperad Payoff Plots ###
def bull_call_plot(sT, bull_call_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT,bull_call_payoff, color = 'g')
    ax.set_title('Bull Call Spread Payoff')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit and loss')
    plt.show()

def bear_call_plot(sT, bear_call_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT,bear_call_payoff, color = 'r')
    ax.set_title('Bear Call Spread Payoff')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit and loss')
    plt.show()

def bull_put_plot(sT, bull_put_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT, bull_put_payoff, color ='lightgreen')
    ax.set_title('Bull Put Spread Payoff')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit & Loss')
    plt.show()

def bear_put_plot(sT, bear_put_payoff ):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT, bear_put_payoff, color ='tomato')
    ax.set_title('Bear Put Spread Payoff')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit & Loss')
    plt.show()

def collar_plot(sT, collar_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT,collar_payoff, color = 'b')
    ax.set_title('Collar Payoff')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit and loss')
    plt.show()

def long_combo_plot(sT, long_combo_payoff):
    fix , ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT,long_combo_payoff,color='royalblue')
    ax.set_title('Long Combo Payoff')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit and loss')
    plt.show()

def straddle_plot(sT, straddle_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT,straddle_payoff, color = 'gold')
    ax.set_title('Straddle Spread Payoff')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit and loss')
    plt.show()

def strangle_plot(sT, strangle_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT,strangle_payoff, color = 'b')
    ax.set_title('Strangle Spread Payoff')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit and loss')
    plt.show()

### Multileg Spread Payoff Plots ###
def bear_call_ladder_plot(sT, bear_call_ladder_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT,bear_call_ladder_payoff,color='peru')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit & Loss')
    plt.show()

def iron_condor_plot(sT, iron_condor_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT,iron_condor_payoff, color = 'peru')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit and loss')
    plt.show()

def butterfly_spread_plot(sT,butterfly_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT,butterfly_payoff ,color='orange')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit & Loss')
    plt.show()

def iron_butterfly_plot(sT, iron_butterfly_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT, iron_butterfly_payoff, color ='brown')
    ax.set_title('Iron Butterfly Spread')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit & Loss')
    plt.show()

def jade_lizard_plot(sT,jade_lizard_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT,jade_lizard_payoff, color = 'lime')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit and Loss')
    plt.show()

# Plot Template
#def _plot(sT, _payoff):
#    fig, ax = plt.subplots()
#    ax.spines['bottom'].set_position('zero')
#    ax.plot(sT,_payoff, color = 'b')
#    ax.set_title(' Payoff')
#    plt.xlabel('Stock Price (sT)')
#    plt.ylabel('Profit and loss')
#    plt.show()

##### Two Leg Spread Payoff Plots with Components #####
def bull_call_payoff_plot(sT, bull_call_spread_payoff, K1_call_payoff, K2_short_call_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT,K1_call_payoff,'--',label='K1 Long Call',color='g')
    ax.plot(sT,K2_short_call_payoff,'--',label='K2 Short Call ',color='r')
    ax.plot(sT,bull_call_spread_payoff,label='Bull Call Spread')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit and loss')
    plt.legend()
    plt.show()

def bear_call_payoff_plot(sT, bear_call_spread_payoff, K1_short_call_payoff, K2_call_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT,K1_short_call_payoff,'--',label='K1 Short Call ',color='r')
    ax.plot(sT,K2_call_payoff,'--',label='K2 Long Call',color='g')
    ax.plot(sT,bear_call_spread_payoff,label='Bear Call Spread')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit and loss')
    plt.legend()
    plt.show()

def bull_put_payoff_plot(sT, bull_put_spread_payoff, put_payoff, short_put_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT, bull_put_spread_payoff, color ='b', label = 'Bull Put Spread')
    ax.plot(sT, put_payoff,'--', color ='g', label ='Long Put')
    ax.plot(sT, short_put_payoff,'--', color ='r', label ='Short Put')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit & Loss')
    plt.legend()
    plt.show()

def bear_put_payoff_plot(sT, bear_put_spread_payoff, put_payoff, short_put_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT, bear_put_spread_payoff, color ='b', label = 'Bear Put Spread')
    ax.plot(sT, put_payoff,'--', color ='g', label ='Long Put')
    ax.plot(sT, short_put_payoff,'--', color ='r', label ='Short Put')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit & Loss')
    plt.legend()
    plt.show()

def collar_payoff_plot(sT, collar__payoff, short_call_payoff, put_payoff):
    fig, ax = plt.subplots()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT, short_call_payoff,'--',label='Short Call',color='r')
    ax.plot(sT, put_payoff,'--',label='Long Put',color='g')
    ax.plot(sT, collar_payoff,label='Protective Collar')
    plt.xlabel('Stock Price (sT)', ha='left')
    plt.ylabel('Profit and loss')
    plt.legend()
    plt.show()

def long_combo_payoff_plot(sT, long_combo_payoff, short_put_payoff, call_payoff):
    fix , ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT,long_combo_payoff,color='b', label = 'Long Combo')
    ax.plot(sT,short_put_payoff,'--',color='r', label = 'Short Put')
    ax.plot(sT,call_payoff,'--',color='g', label = 'Long Call')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit and loss')
    plt.legend()
    plt.show()

def straddle_payoff_plot(sT, straddle_payoff, put_payoff, call_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT,call_payoff,'--',label='Long Call',color='r')
    ax.plot(sT,put_payoff,'--',label='Long Put',color='g')
    ax.plot(sT,straddle_payoff,label='Straddle Sperad')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit and loss')
    plt.legend()
    plt.show()

def strangle_payoff_plot(sT, strangle_payoff, K1_put_payoff, K2_call_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT,K1_put_payoff,'--',label='K1 Long Put',color='r')
    ax.plot(sT,K2_call_payoff,'--',label='K2 Long Call',color='g')
    ax.plot(sT,strangle_spread_payoff,label='Strangle Sperad')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit and loss')
    plt.legend()
    plt.show()

##### Multi Leg Spread Payoff Plots with Components #####
def bear_call_ladder_payoff_plot(sT, bear_call_ladder, call_payoff, K2_call_payoff, short_call_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT, bear_call_ladder, color='b', label= 'Bear Call Ladder')
    ax.plot(sT, call_payoff,'--', color='g',label='ATM Long Call')
    ax.plot(sT, K2_call_payoff,'--', color='g', label='OTM Long Call')
    ax.plot(sT, short_call_payoff, '--', color='r', label='ITM Short call')
    plt.legend()
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit & Loss')
    plt.show()

def iron_condor_payoff_plot(sT, iron_condor_payoff, call_payoff, short_call_payoff, put_payoff, short_put_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT,call_payoff,'--',label='Long K4 Call',color='g')
    ax.plot(sT,short_call_payoff,'--',label='Short K4 Call',color='r')
    ax.plot(sT,put_payoff,'--',label='Long K1 Strike Put',color='y')
    ax.plot(sT,short_put_payoff,'--',label='Short K2 Strike Put',color='m')
    ax.plot(sT,iron_condor_payoff,label='Iron Condor Spread')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit and loss')
    plt.legend()
    plt.show()

def butterfly_payoff_plot(sT, butterfly_spread_payoff, K4_strike_call_payoff, K2_strike_call_payoff, short_call_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT, butterfly_spread_payoff ,color='b', label= 'Butterfly Spread')
    ax.plot(sT, K2_strike_call_payoff,'--', color='g',label='Lower Strike Call')
    ax.plot(sT, K4_strike_call_payoff,'--', color='g', label='Higher Strike Call')
    ax.plot(sT, short_call_payoff, '--', color='r', label='Short Call')
    plt.legend()
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit & Loss')
    plt.show()

def iron_butterfly_payoff_plot(sT, iron_butterfly_payoff, call_payoff, short_call_payoff, put_payoff, short_put_payoff):
    fig, ax = plt.subplots(figsize=(10,5))
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT, iron_butterfly_payoff, color ='b', label ='Iron Butterfly Spread')
    ax.plot(sT, call_payoff,'--', color ='g', label = 'Long Call')
    ax.plot(sT, short_call_payoff,'--', color ='r', label = 'Short Call')
    ax.plot(sT, put_payoff,'--', color ='g',label = 'Long Put')
    ax.plot(sT, short_put_payoff,'--', color ='r',label = 'Short Put')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit & Loss')
    plt.legend()
    plt.show()

def jade_lizard_payoff_plot(sT,jade_lizard_payoff,call_payoff,short_call_payoff,short_put_payoff):
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT,call_payoff,'--',label='Long Strike Call',color='g')
    ax.plot(sT,short_call_payoff,'--',label='Short Strike Call',color='r')
    ax.plot(sT,short_put_payoff,'--',label='Short Strike Put',color='m')
    ax.plot(sT,jade_lizard_payoff,label='Jade Lizard Payoff')
    plt.xlabel('Stock Price (sT)')
    plt.ylabel('Profit and Loss')
    plt.legend()
    plt.show()

##### Implied volatility Calculation #####
def impl_vol(underlying_price, strike, interest_rate, days_to_expiration, call_price):
    iv_calculation = mibian.BS([underlying_price, strike, interest_rate, days_to_expiration],callPrice= call_price)
    return iv_calculation.impliedVolatility

##### Calendar Spread #####
def calendar_spread(sT, interest_rate, strike, front_future, back_future, dte_front_opt, dte_back_opt):
    '''
    Calendar spread involves options of the same underlying & strike price but with different expiry
        If a Call/Put is Sold with near-term expiration it is called "“front-month”"
        If a Call/Put is Bought with long-term expiration it is called "“back-month”"
    '''
    net_premium = back_opt_premium - front_opt_premium
    days_diff = dte_back_opt - dte_front_opt + 1
    # Front-month IV
    front_opt_iv = mibian.BS([front_future, strike, interest_rate, dte_front_opt], callPrice=front_opt_premium).impliedVolatility
    # Back-month IV
    back_opt_iv = mibian.BS([back_future, strike, interest_rate, dte_back_opt], callPrice=back_opt_premium).impliedVolatility
    # Calendar Spread DataFrame
    calendar_spread = pd.DataFrame()
    calendar_spread['underlying_price'] = sT
    calendar_spread['front_opt_premium'] = np.nan
    calendar_spread['back_opt_premium'] = np.nan
    for i in range(0,len(calendar_spread)): # Calculating option price for different possible values of Future Contracts
        calendar_spread.loc[i,'front_opt_premium'] = mibian.BS([calendar_spread.iloc[i]['underlying_price'], strike, interest_rate, dte_front_opt], volatility=front_opt_iv).callPrice
        calendar_spread.loc[i,'back_opt_premium'] = mibian.BS([calendar_spread.iloc[i]['underlying_price']+days_diff, strike, interest_rate, dte_back_opt], volatility=back_opt_iv).callPrice
    calendar_spread['payoff'] = calendar_spread.back_opt_premium - calendar_spread.front_opt_premium - net_premium
    return calendar_spread

def calendar_spread_plot(sT, calendar_spread):
    plt.figure(figsize=(10,5))
    plt.ylabel("Payoff")
    plt.xlabel("Underlying Price (sT)")
    plt.plot(sT,calendar_spread.payoff)
    plt.show()

##### Diagonal Spread #####
def diagonal_spread(sT, interest_rate, front_strike, back_strike, front_future, back_future, dte_front_opt, dte_back_opt):
    '''
    Diagonal spread (similar to a Calendar Spread) involves options of the same underlying but with different strike price & expiry
        If a Call/Put is Sold with near-term expiration it is called "“front-month”"
        If a Call/Put is Bought with long-term expiration it is called "“back-month”"
    '''
    net_premium = back_opt_premium - front_opt_premium
    days_diff = dte_back_opt - dte_front_opt + 1
    # Front-month IV
    front_opt_iv = mibian.BS([front_future, front_strike, interest_rate, dte_front_opt], callPrice=front_opt_premium).impliedVolatility
    # Back-month IV
    back_opt_iv = mibian.BS([back_future, back_strike, interest_rate, dte_back_opt], callPrice=back_opt_premium).impliedVolatility
    # Calendar Spread DataFrame
    diagonal_spread = pd.DataFrame()
    diagonal_spread['underlying_price'] = sT
    diagonal_spread['front_opt_premium'] = np.nan
    diagonal_spread['back_opt_premium'] = np.nan
    for i in range(0,len(diagonal_spread)): # Calculating option price for different possible values of Future Contracts
        diagonal_spread.loc[i,'front_opt_premium'] = mibian.BS([diagonal_spread.iloc[i]['underlying_price'], front_strike, interest_rate, dte_front_opt], volatility=front_opt_iv).callPrice
        diagonal_spread.loc[i,'back_opt_premium'] = mibian.BS([diagonal_spread.iloc[i]['underlying_price']+days_diff, back_strike, interest_rate, dte_back_opt], volatility=back_opt_iv).callPrice
    diagonal_spread['payoff'] = diagonal_spread.back_opt_premium - diagonal_spread.front_opt_premium - net_premium
    return diagonal_spread

def diagnoal_spread_plot(sT, diagonal_spread):
    plt.figure(figsize=(10,5))
    plt.ylabel("Payoff")
    plt.xlabel("Underlying Price (sT)")
    plt.plot(sT,diagonal_spread.payoff)
    plt.show()
