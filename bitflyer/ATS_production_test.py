import urllib
import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pybitflyer
import math

## bitflyer_apiの初期化
api = pybitflyer.API(api_key = "", api_secret = "")
position_status = ["",""]
profit_sum = 0
profit_pre = 0
transaction_count = 0
win = 0
lose = 0
wait_count = 0
order_size = 0.001
size_array = []

a = ["aa","bb"]
if a[0] == "aa":
    a[1] = "cc"
print(a[1])

#api.sendchildorder(product_code="FX_BTC_JPY",child_order_type="MARKET",side="BUY",size=order_size,time_in_force="FOK")
#api.sendchildorder(product_code="FX_BTC_JPY",child_order_type="MARKET",side="SELL",size=order_size,time_in_force="GTC")

#position_now = api.getpositions(product_code="FX_BTC_JPY")
#print(len(position_now))
'''
for j in position_now:
    if j["side"] == "BUY":
        api.sendchildorder(product_code="FX_BTC_JPY",child_order_type="MARKET",side="SELL",size=j["size"],time_in_force="GTC")
    elif j["side"] == "SELL":
        api.sendchildorder(product_code="FX_BTC_JPY",child_order_type="MARKET",side="BUY",size=j["size"],time_in_force="GTC")
    else:
        pass
'''
