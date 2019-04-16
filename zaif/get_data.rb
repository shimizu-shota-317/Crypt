require 'zaif'
require 'json'
require 'pp'
require 'gnuplot'

ZAIF_KEY = ""
ZAIF_SECRET = ""

api = Zaif::API.new(:api_key => ZAIF_KEY, :api_secret => ZAIF_SECRET)
data1 = api.get_info
# ticker -> last:終値、high:過去24時間の高値、low:過去24時間の安値、vwap:過去24時間の加重平均、volume:過去24時間の出来高、bid:買気配値、ask:売気配値
data2 = api.get_ticker("btc")
# 板情報
data3 = api.get_depth("btc")

data1.each { |key,value|
	case key
	when "funds"
		puts " ---買付余力--- "
		puts " JPY : #{value["jpy"]}"
		puts " BTC : #{value["btc"]}"
		puts " MONA : #{value["mona"]}"
	when "deposit"
		puts " ---残高--- "
		puts " JPY : #{value["jpy"]}"
		puts " BTC : #{value["btc"]}"
		puts " MONA : #{value["mona"]}"
	when "trade_count"
		puts "過去の取引回数 : #{value}"
	when "open_orders"
		puts "現在の取引数 : #{value}"

	end
}

puts "-----------------------------------"

data2.each { |key,value|
	case key
	when "last"
		puts " last : #{value} "
	when "high"
		puts " high : #{value} "
	when "low"
		puts " low : #{value} "
	when "vwap"
		puts " vwap : #{value} "
	when "volume"
		puts " volume : #{value} "
	when "bid"
		puts " bid : #{value} "
	when "ask"
		puts " ask : #{value} "
	end
}  

puts "-----------------------------------"

# p data3

puts "-----------------------------------"


