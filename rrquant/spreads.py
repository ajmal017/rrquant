import pandas as pd

#2 Leg Spreads
spread = ['Bull Call', 'Bear Call','Bull Put','Bear Put', 'Protective Collar', 'Straddle', 'Strangle']
leg_1 = ['Long Call @ K1','Short Call @ K1','Short Put @ K1','Long Put @ K1','Long OTM Put @ K1','Long Call @ K1', 'Long Put @ K1']
leg_2 = ['Short Call @ K2', 'Long Call @ K2','Long Put @ K2','Short Put @ K2', 'Short OTM Call @ K2', 'Long Put @ K2','Long Call @ K2']
strike_price = ['K2 > K1', 'K2 > K1', 'K2 < K1', 'K2 < K1','K1 < K2', 'K1 = K2', 'K1 < K2']
debit_credit = ['Debit','Credit','Credit','Debit']
max_gain = ['K2 - K1 - Premium Paid', 'Premium Received','Premium Received','K1 - K2 - Premium Paid']
max_loss = ['Premium Paid','K2 - K1 - Premium Received','K1 - K2 - Premium Received','Premium Paid']
used = ['Reduce Premium Payable',"Reduce Option Position's Risk",'Reduce Premium Payable',"Reduce Option Position's Risk"]

spread_df = pd.DataFrame({'Option Spread':spread, 'Leg 1': leg_1,
    'Leg 2': leg_2, 'Strike Prices': strike_price,'Debit/Credit':debit_credit,
    'Max Gain': max_gain, 'Max Loss':max_loss, 'Purpose': used})
spread_df.loc[spread_df['Option Spread'] == input('Option Spread Strategy:')]

spread_df


#4 Leg Spreads
spread = ['Iron Condor', ]
leg_1 = ['Long OTM Put @ K1', ]
leg_2 = ['Short OTM Put @ K2', ]
leg_3 = ['Short OTM Call @ K3', ]
leg_4 = ['Long OTM Call @ K4',]
strike_price = ['K1 < K2 < K3 < K4 (Where K2 - K1 = K4 - K3)',]
debit_credit = ['Debit',]
max_gain = ['K2 - K1 - Premium Paid',]
max_loss = ['Premium Paid',]
used = ['Reduce Premium Payable',]

spread_df = pd.DataFrame({'Option Spread':spread, 'Leg 1': leg_1,
    'Leg 2': leg_2, 'Strike Prices': strike_price,'Debit/Credit':debit_credit,
    'Max Gain': max_gain, 'Max Loss':max_loss, 'Purpose': used})
spread_df.loc[spread_df['Option Spread'] == input('Option Spread Strategy:')]
