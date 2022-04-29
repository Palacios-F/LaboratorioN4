import ccxt
import pandas as pd
import numpy as np
import time

#auxiliar functions
ccxt_time_conv = lambda x: x[:16].replace('T',' ')
get_actual_time = lambda : time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
merge_join = lambda a,b:  pd.merge(a,b,how = 'inner',on = 'TimeStamp') #auxiliar function to join to tables
diff = lambda ts: np.diff(ts) # auxiliar function to calculate the difference in a array
roll = lambda Pt,nn: 2*(abs(np.cov(diff(Pt)[:nn],diff(Pt)[-nn-1:-1])[0,1]))**0.5 #auxiliar function to calcule Roll's spread

def timer(function, ntimes,*args):
    """
    Function to calculate time spending by a function
    
            Parameters:
                function
    """
    start = time.time()
    function(*args)
    end = time.time()
    return end - start

def get_order(exchanges, limit, ticker):
    """
    Function to calculate the order book o a ticker using differents exchanges
    """
    orderbook = [exchanges[i].fetch_order_book(ticker[str(exchanges[i])],limit) for i in range(len(exchanges))]
    return orderbook

def get_ob_time(exchanges, limit, tickets, time_delay, minutes):
    """
    Generalization of get_order using different exchanges, at the same time gets the infor during
    a time period, and consider the time spended by the function
    """
    data = []
    time_array = []
    for n in range(minutes):
      time_frame = []
      time_array.append(get_actual_time())
      for ticket in tickets:
        ticker_ob = get_order(exchanges,limit, ticket)
        time_frame.append(ticker_ob)
      data.append([time_frame])
      time.sleep(time_delay)
    return data,time_array

def converter(data, time_array, exchanges, tickets):
    """
    Convert the data from get_ob_time in a dataframe 
    """
    n = len(data)
    m = len(data[0][0])
    nn = len(data[0][0][0])

    data_f = pd.DataFrame(columns = ['Ticker', 'Exchange', 'TimeStamp', 'Level','Bid','Ask','Spread', 'Bid_volume','Ask_volume','Total_volume', 'Mid_price','VWAP'])
    for i in range(nn):
      for j in range(m):
        data_t = np.zeros([n,9])
        for h in range(n):
          frame = data[h][0][j][i]
          bid = frame['bids'][0][0] if len(frame['bids']) > 0 else None
          ask = frame['asks'][0][0] if len(frame['asks']) >0 else None
          spread = (ask- bid) if (ask and bid) else None
          volume_bid = np.transpose(np.array(frame['bids']))[1].sum()
          volume_ask = np.transpose(np.array(frame['asks']))[1].sum()
          level = len(np.transpose(np.array(frame['bids']))[1])
          total_volume = volume_bid+volume_ask
          mean_price = (np.transpose(np.array(frame['asks']))[0].mean() +np.transpose(np.array(frame['asks']))[0].mean())/2
          mid_price = (bid+ask)/2
          data_t[h,:] = [level,bid,ask,spread,volume_bid,volume_ask, total_volume, mid_price, mean_price]
        ticket_frame = pd.DataFrame(data = data_t,columns = ['Level','Bid','Ask','Spread', 'Bid_volume','Ask_volume','Total_volume', 'Mid_price','Mean'])
        ticket_frame['Ticker'] = tickets[j]
        ticket_frame['Exchange'] = exchanges[i]
        ticket_frame['TimeStamp'] = time_array
        ticket_frame['VWAP'] = (ticket_frame.Mean*ticket_frame.Total_volume).cumsum()/ticket_frame.Total_volume.cumsum()
        ticket_frame.drop(columns = ['Mean'], inplace = True)
        data_f = data_f.append(ticket_frame, ignore_index = True)
  
    return data_f

def order_book_converter(data,exchanges, tickets):
    """
    Convert the data from get_ob_time in a dataframe and get the orderbook to be used
    in a animation
    """
    n = len(data)
    m = len(data[0][0])
    nn = len(data[0][0][0])
    dic_data = {}
    for i in range(nn):
      for j in range(m):
        M = []
        combination = exchanges[i] + " | "+tickets[j] 
        for h in range(n):
          frame = data[h][0][j][i]
          frame_ask = pd.DataFrame(frame['asks'], columns =['price', 'volume'])
          frame_ask['type'] = 'ask'
          frame_bid = pd.DataFrame(frame['bids'], columns = ['price', 'volume'])
          frame_bid['type'] = 'bid'
          frame_ob = frame_bid.append(frame_ask, ignore_index=True)
          M.append(frame_ob)
        dic_data[combination] = M
    return dic_data

def get_ohlc(exchanges,ticker,time_f,since,minute_limit ):
    """
    Function that returns the ohlc given one ticker and a list of exchanges
    """
    ohlc = []
    for i in range(len(exchanges)):
      ohlc_t = pd.DataFrame(exchanges[i].fetch_ohlcv(ticker[str(exchanges[i])],time_f,since,minute_limit),columns = ['TimeStamp','open','high','close','low','Volume'])
      ohlc_t['TimeStamp'] = ohlc_t.TimeStamp.map(lambda x: ccxt_time_conv(ccxt.bitso.iso8601(x)))
      ohlc.append(ohlc_t)
    return ohlc

def get_ohlc_all(exchanges, tickets,time_f,since,minute_limit):
    """
    Generalization of get_ohlc to different Tickers
    """
    ticker_array = []
    for ticket in tickets:
      ticker_ob = get_ohlc(exchanges,ticket,time_f,since,minute_limit )
      ticker_array.append(ticker_ob)
    return ticker_array 


def Roll(Time_S, initial_point, n_points,fixed_points):
    """
    Generalization of Roll'S Spread to a Time Series
    """
    n = len(Time_S)
    out = np.zeros(n)
    for i in range(initial_point+1,n):
      out[i] = roll(Time_S[i-n_points-1:i],fixed_points)
    return out

def merge_all(data1,data2, exchanges, tickers, mapf, function,name,column, *args):
    """
    function to combine OHLC and Order Book data
    """
    data_f = pd.DataFrame(columns = ['Ticker', 'Exchange', 'TimeStamp','Spread', 'close'])

    for j in range(3):
      for i in range(3):
        df1 = data1[((data1.Ticker == tickers[j]) & (data1.Exchange ==exchanges[i]))]
        df2 = data2[j][i]
        df3 = merge_join(df1.loc[:,['Ticker','Exchange','TimeStamp','Spread']],df2.loc[:,['TimeStamp','close']])
        if mapf == True:
          df3[name] = Roll(df3[column],*args)
        data_f = data_f.append(df3, ignore_index = True)
    return data_f