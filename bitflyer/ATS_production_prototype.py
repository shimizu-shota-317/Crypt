#------------------------------------------------------------#
import urllib
import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pybitflyer
import math
#------------------------------------------------------------#

## いなごflyerの初期化
weight = 2
sell_volume_array = []
buy_volume_array = []
driver = webdriver.PhantomJS()
driver.get("https://inagoflyer.appspot.com/btcmac")

## bitflyer_apiの初期化
api = pybitflyer.API(api_key = "", api_secret = "")
position_status = ["",""]
position_init = api.getpositions(product_code="FX_BTC_JPY")
if len(position_init) == 0:
    position_status[0] = "empty"
    position_status[1] = "none"
elif len(position_init) >= 1:
    position_status[0] = "positioned"
    position_status[1] = "???"
else:
    pass

#------------------------------------------------------------#

threshold = 250
difference = 100
order_size = 0.1

#------------------------------------------------------------#

profit_sum = 0
profit_pre = 0
transaction_count = 0
win = 0
lose = 0
size_array = []
first_flag = 1

# webページの値が安定するまでT秒待つ
T = 5
for num1 in range(T):
    print("ロード中：残り" + str(T-num1) + "秒")
    time.sleep(1)
print("----------------------------------------------------")
# 時間の計測を開始
start = time.time()

###------------------------------------------------------------###
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

    elapsed_time = time.time() - start
    if elapsed_time > 5:
        first_flag = 0

##------------------------------------------------------------##

    # 現在の状況を出力
    print("経過時間：" + str(int(elapsed_time)) + "秒")
    print("売り：" + str(sell_volume_sum) + " " + "買い：" + str(buy_volume_sum))
    #print('売り：' + str(sell_volume) + " " + "買い：" + str(buy_volume))
    print("現在の比率幅：" + "%.5f" % ratio_weight)
    print("取引回数：" + str(transaction_count) + "回")
    #print("勝ち：" + str(win) + "回" + " " + "負け：" + str(lose)+ "回")
    print("ポジション：" + str(position_status[0]))
    print("ポジションタイプ：" + str(position_status[1]))
    #print("直前の利益：" + str(int(profit_pre)) + "円" + " " + "総利益：" + str(int(profit_sum)) + "円")
    print("----------------------------------------------------")

##------------------------------------------------------------##

# 注文アルゴリズム
#------------------------------------------------------------#
    if position_status[0] == "empty":
        if ratio_weight > 0 and buy_volume_sum > threshold and (buy_volume_sum / sell_volume_sum) > 2.2 and first_flag == 0:
            try:
                health = api.gethealth(product_code="FX_BTC_JPY")
            except:
                print("混雑状況の取得を失敗")
                print("----------------------------------------------------")
            if health["status"] == "NORMAL":
                try:
                    order = api.sendchildorder(product_code="FX_BTC_JPY",child_order_type="MARKET",side="BUY",size=order_size,time_in_force="FOK")
                except:
                    print("注文失敗")
                    print("----------------------------------------------------")
                else:
                    if "child_order_acceptance_id" in order:
                        acceptance_id = order["child_order_acceptance_id"]
                        position_status[0] = "waiting"
                        position_status[1] = "BUY"
                    else:
                        print("注文IDが取得できません")
                        print("----------------------------------------------------")
            else:
                print(health["status"])

        if ratio_weight < 0 and sell_volume_sum > threshold and (sell_volume_sum / buy_volume_sum) > 2.2 and first_flag == 0:
            try:
                health = api.gethealth(product_code="FX_BTC_JPY")
            except:
                print("混雑状況の取得を失敗")
                print("----------------------------------------------------")
            if health["status"] == "NORMAL":
                try:
                    order = api.sendchildorder(product_code="FX_BTC_JPY",child_order_type="MARKET",side="SELL",size=order_size,time_in_force="FOK")
                except:
                    print("注文失敗")
                    print("----------------------------------------------------")
                else:
                    if "child_order_acceptance_id" in order:
                        acceptance_id = order["child_order_acceptance_id"]
                        position_status[0] = "waiting"
                        position_status[1] = "SELL"
                    else:
                        print("注文IDが取得できません")
                        print("----------------------------------------------------")
            else:
                print(health["status"])

#------------------------------------------------------------#
    if position_status[0] == "waiting":
        time_begin_waiting = time.time();
        while True:
            for num3 in range(5):
                try:
                    executions = api.getexecutions(product_code="FX_BTC_JPY",child_order_acceptance_id=acceptance_id)
                except:
                    print("データを取得できません")
                    print("----------------------------------------------------")
                    time.sleep(3)
                else:
                    break

                print(executions)
            waiting_time = time.time() - time_begin_waiting
            if len(executions) >= 1:
                position_status[0] = "positioned"
                position_status[1] = executions[0]["side"]
                break
            elif len(executions) == 0:
                print("約定が確認できません")
                print("----------------------------------------------------")

            if waiting_time > 300:
                position_status[0] = "empty"
                position_status[1] = "none"
                print("一定時間約定が確認できなかった為、約定がキャンセルされたと判断します")
                print("----------------------------------------------------")
                break
            time.sleep(1)

#------------------------------------------------------------#
    if position_status[0] == "positioned":
        if (position_status[1] == "BUY" and ratio_weight < 1) or (position_status[1] == "SELL" and ratio_weight > -1):
            if executions[0]["side"] == "SELL":
                side = "BUY"
            elif executions[0]["side"] == "BUY":
                side = "SELL"

            try:
                order_out = api.sendchildorder(product_code="FX_BTC_JPY",child_order_type="MARKET",side=side,size=order_size,time_in_force="FOK")
            except:
                print("注文失敗")
                print("----------------------------------------------------")
            else:
                if "child_order_acceptance_id" in order_out:
                    acceptance_id_out = order_out["child_order_acceptance_id"]
                    position_status[0] = "waiting_out"
                else:
                    print("注文IDが取得できません")
                    print("----------------------------------------------------")

#------------------------------------------------------------#
    if position_status[0] == "waiting_out":
        time_begin_waiting_out = time.time();
        while True:
            for num6 in range(5):
                try:
                    executions_out = api.getexecutions(product_code="FX_BTC_JPY",child_order_acceptance_id=acceptance_id_out)
                except:
                    print("データを取得できません")
                    print("----------------------------------------------------")
                    time.sleep(2)
                else:
                    break

            waiting_out_time = time.time() - time_begin_waiting_out
            if len(executions_out) >= 1:
                position_status[0] = "empty"
                position_status[1] = "none"
                transaction_count = transaction_count + 1
                break
            else:
                print("ポジションが残っています")
                print("----------------------------------------------------")

            if waiting_out_time > 300:
                position_status[0] = "positioned"
                print("一定時間約定が確認できなかった為、約定がキャンセルされたと判断します")
                print("----------------------------------------------------")
                break
            time.sleep(1)
#------------------------------------------------------------#
    time.sleep(1)
#------------------------------------------------------------#
