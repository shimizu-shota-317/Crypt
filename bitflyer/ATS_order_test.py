#------------------------------------------------------------#
import urllib
import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pybitflyer
import math
#------------------------------------------------------------#
## bitflyer_apiの初期化
api = pybitflyer.API(api_key = "", api_secret = "")
position_status = ["",""]
position_init = api.getpositions(product_code="FX_BTC_JPY")
#------------------------------------------------------------#
order_size = 0.001

order = api.sendchildorder(product_code="FX_BTC_JPY",child_order_type="MARKET",side="BUY",size=order_size,time_in_force="FOK")
acceptance_id = order["child_order_acceptance_id"]

while True:
    time.sleep(3)
    executions = api.getexecutions(product_code="FX_BTC_JPY",child_order_acceptance_id=acceptance_id)
    if len(executions)>=1:
        position_status[0] = "positioned"
        position_status[1] = executions[0]["side"]
        break

print(str(position_status[0]) + " " + str(position_status[1]))
