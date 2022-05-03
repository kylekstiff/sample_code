import tda;
import csv;
import json;
import time;
import pandas;
import datetime as dt;
import mplfinance as mpf;
import pandas_datareader as pd;
import matplotlib.pyplot as plt;
import matplotlib.dates as mdate;
from selenium import webdriver;
from tda import auth, client;
from tda.auth import easy_client;
from tda.client import Client;
from tda.streaming import StreamClient;

import asyncio;

from urllib.request import Request, urlopen;

def convert_epoch_to_usefultime(my_time):

    seconds = int(my_time/1000)
    dat = dt.date.fromtimestamp(seconds)
    return dat

def gap_finder(close, next_day_open):

  gap = int(((next_day_open - close)/close) * 100)
  return f"{gap}%"

# input list to scan : watchlist
# watchlist = ['SOPA']
def lf_finder(feed):

  with open(feed) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    for row in csv_reader:
        line_count =+ 1
        if (line_count % 50) == 0:
          time.sleep(3)
        url = f'https://api.tdameritrade.com/v1/marketdata/{row[0]}/pricehistory?apikey=GRNCGVIHW0DHNLG7OGQVJJBIGC7CN46G&periodType=year&period=1&frequencyType=daily'
        request = Request(url)

        json_byte = urlopen(request).read()
        json_obj = json.loads(json_byte)

        this = json_obj['candles']

        for day in range(len(this)-1):
          if this[day+1]['open'] >= (this[day]['close'] * 1.30):

            f = open("./lowfloat_gappers.csv", "a")
            f.write(f"{row[0]},{(gap_finder(this[day]['close'], this[day+1]['open']))},{convert_epoch_to_usefultime(this[day+1]['datetime'])},{int(this[day+1]['datetime'])},{int(this[day+1]['datetime'])+54000000}\n")
            f.close()
            
        # for day in range(len(this)):
        #     if this[day]['high'] - this[day]['open'] >= (ATR.find_average_true_range(symbol)): pointer = this[day]
        #     if pointer != 0:
        #         if this[day]['open'] > pointer['high'] or this[day]['open'] < pointer['low'] or this[day]['close'] > pointer['high'] or this[day]['close'] < pointer['low']: pointer = 0

        # if pointer != 0:
        #     return_dict['stonks'].append(symbol)
      
  return 0

for x in range(1, 85):
  lf_finder(f"./files/{x}.csv")
  time.sleep(10)
# lf_finder(f"./files/10.csv")

# async def read_stream():
#     return_item = find_gaps_down(watch_list)
#     list_to_open = []
    
#     for x in return_item['stonks']:
#         list_to_open.append(x['ticker'])
#         print(x['ticker'])
    
#     await stream_client.login()
#     await stream_client.quality_of_service(StreamClient.QOSLevel.EXPRESS)

#     # Always add handlers before subscribing because many streams start sending
#     # data immediately after success, and messages with no handlers are dropped.
#     stream_client.add_chart_equity_handler(handler)
#     await stream_client.chart_equity_subs(list_to_open)


#     while True:
#         await stream_client.handle_message()

# asyncio.run(read_stream())


# ---------------------------------------


# given_ticker = input("Ticker? ").upper().strip(" ")


# print(json_obj)


# async def hello():
#     uri = 'wss://ws.twelvedata.com/v1/quotes/price?apikey=c4ba3a1cbbed4000942925d36762e0cb'


#     async with websockets.connect(uri) as websocket:

#         raw_auth = {
#             "action": "subscribe", 
#             "params": {
#                 "symbols": "AAPL,RY,RY:TSX,EUR/USD,BTC/USD"
#             }
#         }
#         send_auth = json.dumps(raw_auth)

#         await websocket.send(send_auth)
#         this = await websocket.recv()
#         print(this)

#         # raw_sub = {"action":"subscribe","params":"T.LPL"}
#         # send_sub = json.dumps(raw_sub)

#         # await websocket.send(send_sub)
#         # this = await websocket.recv()
#         # print(this)


# asyncio.get_event_loop().run_until_complete(hello())


# hold_this = json_obj['candles']


buy_points = []

# for index, candle in enumerate(hold_this):
#     if hold_this[index]['open'] < hold_this[index-1]['close']:
#         if hold_this[index]['high'] >= hold_this[index-1]['low']:
#             buy_point = hold_this[index-1]['low']
#             buy_points.append(buy_point)
#             print(f'Bought {given_ticker} at {hold_this[index-1]["low"]} on {convert_epoch_to_usefultime(hold_this[index]["datetime"])}.')
#         if hold_this[index]['close'] < hold_this[index]['open']:
#             print(f'Sold {given_ticker} same day.')
#     if buy_points != []:
#         print(buy_points)
#         if candle['low'] <= buy_points[0]:
#             print(f'Sold {given_ticker} at {buy_point}.')
#             buy_points = buy_points[::-1].pop()
#             print(buy_points)
        

# Consider: 
    # when do you buy? the daily candle forms over a while so have to drill into daily charts.
    # Are they strongest when there is no bottom wick? Candle characteristics..
    # build a list of stocks w/ ADR > 3% to choose from? for both scripts?
    # other scanner criteria? top 10-20 vol/RVOL? UP 0.5ATR+

    # Scanner:
    # -- check for stocks gapping down under previous day's low
    # -- include %YTD, %6MO, %3MO, %1MO for further screening
    # UNDER 30 RSI INTERESTING FOR REVERSAL W/ THIS?
# # Load data
# url = f'https://api.tdameritrade.com/v1/marketdata/{given_ticker}/pricehistory?apikey=GRNCGVIHW0DHNLG7OGQVJJBIGC7CN46G&periodType=day&period=10&frequencyType=minute&frequency=5&needExtendedHoursData=false'
# print(url)

# request = Request(url)
# json_byte = urlopen(request).read()
# json_obj = json.loads(json_byte)