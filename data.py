import functions as fun
import numpy as np
import ccxt
import warnings
warnings.filterwarnings("ignore")

# list of exchanges
bitso = ccxt.bitso()
ftx = ccxt.ftx()
binance = ccxt.binance()
exa = [bitso, ftx, binance] 

# limit in order book
limit = 30

from_datime = '2022-04-28T19:14:00.000Z' #stampdate to use in OHLC
since = bitso.parse8601(from_datime) #transformation of from_datime to be used in OHLC

# Dictionaries with the tickers used in every exchange
dic_btc = {str(bitso):'BTC/USDT',str(ftx):'BTC/USDT',str(binance):'BTC/USDT'}
dic_eth = {str(bitso):'ETH/USD',str(ftx):'ETH/USD',str(binance):'ETH/USDT'}
dic_sol = {str(bitso):'SOL/USD',str(ftx):'SOL/USD',str(binance):'SOL/USDT'}

# Order Book data previosly run from the 
testeo_time = np.load('files/time.npy').tolist()
testeo = np.load('files/file.npy', allow_pickle='TRUE')

#Order book transformed
df = fun.converter(testeo,testeo_time,[str(bitso),str(ftx),str(binance)],['BTC USD','ETH USD','SOL USD'])

#OHLC data for the same time that Order book
ohlc = fun.get_ohlc_all(exa,[dic_btc, dic_eth, dic_sol],'1m',since,94)

#data of the spread
spread_data = fun.merge_all(df,ohlc,[str(bitso),str(ftx),str(binance)],['BTC USD','ETH USD','SOL USD'],True,
                            fun.Roll,'Effective Spread','close',11,11,5)

#data for the animation
data_books = fun.order_book_converter(testeo,[str(bitso),str(ftx),str(binance)],['BTC USD','ETH USD','SOL USD'])

#data for the graphs configuration
exchange = ['bitso','ftx','binance']
colors = ['#FF5733','#1B68A1','#FFDF2D']
colors2 = ['#FF5733','#1B68A1','#FFDF2D','#7186A9']
colors3 = ['#FF5733','#1B68A1']