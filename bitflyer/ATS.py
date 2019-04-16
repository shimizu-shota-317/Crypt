import urllib
import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pybitflyer
import math

## いなごflyerの初期化
count = 0
weight = 2
sell_volume_array = []
buy_volume_array = []
driver = webdriver.PhantomJS()
driver.get("https://inagoflyer.appspot.com/btcmac")

## bitflyer_apiの初期化
api = pybitflyer.API(api_key = "", api_secret = "")
count_three = False
confirm_position = False
position_status = False
position_type = ""
profit_sum = 0
profit_pre = 0
transaction_count = 0
win = 0
lose = 0
wait_count = 0

# webページの値が安定するまでT秒待つ
T = 10
for num in range(T):
    print("ロード中：残り" + str(T-num) + "秒")
    time.sleep(1)
print("----------------------------------------------------")
start = time.time()
# 1秒ごとにいなごflyerで出来高を取得
while True:

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    sell_volume = soup.find_all('span',class_='lastprice_span')[0].text
    buy_volume = soup.find_all('span',class_='lastprice_span')[1].text

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
    #print("売り：" + str(sell_volume_sum) + " " + "要素数：" + str(len(sell_volume_array)))
    #print("買い：" + str(buy_volume_sum) + " " + "要素数：" + str(len(buy_volume_array)))
    elapsed_time = time.time() - start
    print("経過時間：" + str(int(elapsed_time)) + "秒")
    print("売り：" + str(sell_volume_sum) + " " + "買い：" + str(buy_volume_sum))
    #print('売り：' + str(sell_volume) + " " + "買い：" + str(buy_volume))
    #print("重み付け比率：" + "%.5f" % ratio_weight)
    print("現在の比率幅：" + "%.5f" % ratio_weight)
    #print(count)
    #print(count_three)
    print("取引回数：" + str(transaction_count) + "回")
    print("勝ち：" + str(win) + "回" + " " + "負け：" + str(lose)+ "回")
    print("ポジション：" + str(position_type))
    print("直前の利益：" + str(int(profit_pre)) + "円" + " " + "総利益：" + str(int(profit_sum)) + "円")
    print("----------------------------------------------------")

    for k in range(20):
        try:
            ticker = api.ticker(product_code="FX_BTC_JPY")
        except:
            time.sleep(3)
            print("接続切れ？")
            print("----------------------------------------------------")
        else:
            break

    # シミュレーション
    if ratio_weight > 0 and buy_volume_sum > 250 and (buy_volume_sum - sell_volume_sum) > 100:
        if position_status == False:
            time.sleep(10)
            position_buy_value_long = ticker["best_ask"]
            position_buy_size_long = 0.1
            position_status = True
            position_type = "long"
    if ratio_weight < 0 and sell_volume_sum > 250 and (sell_volume_sum - buy_volume_sum) > 100:
        if position_status == False:
            time.sleep(10)
            position_sell_value_short = ticker["best_bid"]
            position_sell_size_short = 0.1
            position_status = True
            position_type = "short"
    if position_status == True:
        if position_type == "long":
            if ratio < 0:
                time.sleep(10)
                position_sell_value_long = ticker["best_bid"]
                position_sell_size_long = position_buy_size_long
                position_status = False
                position_type = ""
                profit_long = (position_sell_value_long - position_buy_value_long) * position_sell_size_long
                if profit_long < 0:
                    lose = lose + 1
                else:
                    win = win + 1
                profit_pre = profit_long
                profit_sum = profit_sum + profit_long
                transaction_count = transaction_count + 1
        elif position_type == "short":
            if ratio > 0:
                time.sleep(10)
                position_buy_value_short = ticker["best_ask"]
                position_buy_size_short = position_sell_size_short
                position_status = False
                position_type = ""
                profit_short = (position_sell_value_short - position_buy_value_short) * position_buy_size_short
                if profit_short < 0:
                    lose = lose + 1
                else:
                    win = win + 1
                profit_pre = profit_short
                profit_sum = profit_sum + profit_short
                transaction_count = transaction_count + 1
        else:
            pass

    time.sleep(1)
    count = count + 1;
