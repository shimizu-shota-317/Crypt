import urllib
import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
import time

weight = 3
sell_volume_array = []
buy_volume_array = []
driver = webdriver.PhantomJS()
driver.get("https://inagoflyer.appspot.com/btcmac")

for num in range(30):
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # n = soup.find('span',id_='sellVolumePerMeasurementTime')
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

    ratio_weight = buy_volume_sum / (sell_volume_sum + 0.1)
    ratio = buy_volume / (sell_volume + 0.01)

    print(str(num+1) + '回目')
    print('売り：' + str(sell_volume_sum) + ' ' + '要素数：' + str(len(sell_volume_array)))
    print('買い：' + str(buy_volume_sum) + ' ' + '要素数：' + str(len(buy_volume_array)))
    print("重み付け比率：" + "%.5f" % ratio_weight)
    print("現在の比率：" + "%.5f" % ratio)

    time.sleep(1)
