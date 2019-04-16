import urllib
import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pybitflyer
import math

## いなごflyerの初期化
weight = 2
sell_volume_array = []
buy_volume_array = []
driver = webdriver.PhantomJS()
driver.get("https://inagoflyer.appspot.com/btcmac")

## bitflyer_apiの初期化
api = pybitflyer.API(api_key = "", api_secret = "")
position_status = ["",""]
profit_sum = 0
profit_pre = 0
transaction_count = 0
win = 0
lose = 0
wait_count = 0
order_size = 0.01
size_array = []

# webページの値が安定するまでT秒待つ
T = 10
for num in range(T):
    print("ロード中：残り" + str(T-num) + "秒")
    time.sleep(1)
print("----------------------------------------------------")
# 時間の計測を開始
start = time.time()
# いなごflyerで出来高を取得
while True:

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    try:
        sell_volume = soup.find_all('span',class_='lastprice_span')[0].text
    except:
        sell_volume = 0
    try:
        buy_volume = soup.find_all('span',class_='lastprice_span')[1].text
    except:
        buy_volume = 0

    sell_volume = float(sell_volume)
    buy_volume = float(buy_volume)

    sell_volume_array.append(sell_volume)
    buy_volume_array.append(buy_volume)
    if len(sell_volume_array) > weight:
        sell_volume_array.pop(0)
    if len(buy_volume_array) > weight:
        buy_volume_array.pop(0)

    sell_volume_sum = int(sum(sell_volume_array))
    buy_volume_sum = int(sum(buy_volume_array))
    ratio_weight = buy_volume_sum / (sell_volume_sum + 0.00001)
    ratio_weight = math.log2(ratio_weight+0.00001)
    ratio = buy_volume / (sell_volume + 0.00001)
    ratio = math.log2(ratio+0.00001)

    # 現在の状況を出力
    elapsed_time = time.time() - start
    print("経過時間：" + str(int(elapsed_time)) + "秒")
    print("売り：" + str(sell_volume_sum) + " " + "買い：" + str(buy_volume_sum))
    #print('売り：' + str(sell_volume) + " " + "買い：" + str(buy_volume))
    print("現在の比率幅：" + "%.5f" % ratio_weight)
    print("取引回数：" + str(transaction_count) + "回")
    #print("勝ち：" + str(win) + "回" + " " + "負け：" + str(lose)+ "回")
    print("ポジション：" + str(position_status[0]))
    #print("直前の利益：" + str(int(profit_pre)) + "円" + " " + "総利益：" + str(int(profit_sum)) + "円")
    print("----------------------------------------------------")

# 注文アルゴリズム
    if position_status[0] = "empty":
        if ratio_weight > 0 and buy_volume_sum > 250 and (buy_volume_sum - sell_volume_sum) > 100:
            api.sendchildorder(product_code="BTC_JPY",child_order_type="MARKET",side="BUY",size=order_size,time_in_force="FOK")
            position_status = ["waiting","long"]
        if ratio_weight < 0 and sell_volume_sum > 250 and (sell_volume_sum - buy_volume_sum) > 100:
            api.sendchildorder(product_code="BTC_JPY",child_order_type="MARKET",side="SELL",size=order_size,time_in_force="FOK")
            position_status = ["waiting","short"]

    if position_status[0] == "waiting":
        time.sleep(3)
        position_now = api.getpositions()
        if len(position_now) >= 1:
            for i in position_now:
                size_array.append(i["size"])
            if sum(size_array) == order_size:
                position_status[0] = "positioned"
            else:
                print("error")
        wait_count = wait_count + 1
        if wait_count == 3:
            position_status[0] = "empty"
            wait_count = 0

    if position_status[0] == "positioned":
        if position_status[1] == "long":
            if ratio < 0:
                for j in position_now:
                    if j["side"] == "BUY":
                        api.sendchildorder(product_code="BTC_JPY",child_order_type="MARKET",side="SELL",size=j["size"],time_in_force="GTC")
                    elif j["side"] == "SELL":
                        api.sendchildorder(product_code="BTC_JPY",child_order_type="MARKET",side="BUY",size=j["size"],time_in_force="GTC")
                    else:
                        pass
                time.sleep(5)
                position_status[0] = "empty"
                transaction_count = transaction_count + 1
        if position_status[1] == "short":
            if ratio > 0:
                for j in position_now:
                    if j["side"] == "BUY":
                        api.sendchildorder(product_code="BTC_JPY",child_order_type="MARKET",side="SELL",size=j["size"],time_in_force="GTC")
                    elif j["side"] == "SELL":
                        api.sendchildorder(product_code="BTC_JPY",child_order_type="MARKET",side="BUY",size=j["size"],time_in_force="GTC")
                    else:
                        pass
                time.sleep(5)
                position_status[0] = "empty"
                transaction_count = transaction_count + 1

    time.sleep(1)
