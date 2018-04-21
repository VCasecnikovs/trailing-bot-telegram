import telebot,json,os
from urllib import request
from multiprocessing import Process
#from binance.client import Client
bot = telebot.TeleBot("565397863:AAFIvwTm_QE5CYGu_bRSHh6paZWpltM_zMc")
#This function adds json of user. It contains message id, username, transactions list, api and secret key. This json is added to q.vadim file
@bot.message_handler(regexp= "new_member\s[A-Za-z0-9]{16}\s[A-Za-z0-9]{16}")
def a1(msg):
	msg_text = msg.text.split(" ")
	with open("q.vadim", "r") as outfile:	
		main_file = json.load(outfile)
	person = {"name" : msg.from_user.first_name, "id" : msg.from_user.id,"secret":msg_text[1], "api":msg_text[2]}
	main_file[msg.from_user.id] = person
	with open("q.vadim", "w") as outfile:
		json.dump(main_file, outfile)
	bot.send_message(msg.from_user.id, "You are added")

@bot.message_handler(regexp = "add_transaction\s[A-Z]{3,10}\sTR\s[0-9]{1,2}")
def a2(msg):
	with open("q.vadim", "r") as outfile:
		main_file = json.load(outfile)

	msg_text = msg.text.split(" ")
	main_file["trades"].append({"owner_id":msg.from_user.id, "ticker":msg_text[1], "trailing_stop_percent":msg_text[3], "local_maximum": 0, "is_down":False})
	with open("q.vadim","w") as outfile:
		json.dump(main_file, outfile)
	bot.send_message(msg.from_user.id, "Your order is added")

def main_loop():
	while True:
		update_prices()
		find_orders_to_close()


def update_prices():
	#Requesting prices from binance
	request_answer = json.loads(request.urlopen("https://api.binance.com/api/v3/ticker/price").read().decode("utf-8"))
	#Opening JSON file
	with open("q.vadim", "r") as outfile:
		main_file = json.load(outfile)
	
	for symbol in request_answer:
		#Updating price_now
		main_file["price_now"][symbol["symbol"]] = float(symbol["price"])
		#Looking if the price_now is more than max_price
		if main_file["price_now"][symbol["symbol"]] > main_file["highest_price"][symbol["symbol"]]:
			main_file["highest_price"][symbol["symbol"]] = main_file["price_now"][symbol["symbol"]]
		#Calculating percentes
		main_file["percent"][symbol["symbol"]] = 1 - main_file["price_now"][symbol["symbol"]]/main_file["highest_price"][symbol["symbol"]]
	#Saving JSON file
	with open("q.vadim", "w") as outfile:
		json.dump(main_file,outfile)

def find_orders_to_close():
	with open("q.vadim", "r") as outfile:
		main_file = json.load(outfile)
	if main_file["trades"] != []:

		for i in range(len(main_file["trades"])):
			trade = main_file["trades"][i]
			if trade["is_down"] == True:
				continue
			if main_file["price_now"][trade["ticker"]] >  trade["local_maximum"]:
				trade["local_maximum"] = main_file["price_now"][trade["ticker"]]
			if float(trade["trailing_stop_percent"]) <=  (1 - main_file["price_now"][trade["ticker"]]/trade["local_maximum"])*100:
				close_orders(i, trade)
				trade["is_down"]= True
			main_file["trades"][i] = trade
	with open("q.vadim", "w") as outfile:
		json.dump(main_file,outfile)


def close_orders(order, trade):
	bot.send_message(trade["owner_id"], trade['ticker'])


if __name__ == "__main__":
	if not os.path.isfile("q.vadim"):
		with open("q.vadim", "w") as outfile:
			json.dump({"highest_price" : {'ETHBTC': 0, 'LTCBTC': 0, 'BNBBTC': 0, 'NEOBTC': 0, 'QTUMETH': 0, 'EOSETH': 0, 'SNTETH': 0, 'BNTETH': 0, 'BCCBTC': 0, 'GASBTC': 0, 'BNBETH': 0, 'BTCUSDT': 0, 'ETHUSDT': 0, 'HSRBTC': 0, 'OAXETH': 0, 'DNTETH': 0, 'MCOETH': 0, 'ICNETH': 0, 'MCOBTC': 0, 'WTCBTC': 0, 'WTCETH': 0, 'LRCBTC': 0, 'LRCETH': 0, 'QTUMBTC': 0, 'YOYOBTC': 0, 'OMGBTC': 0, 'OMGETH': 0, 'ZRXBTC': 0, 'ZRXETH': 0, 'STRATBTC': 0, 'STRATETH': 0, 'SNGLSBTC': 0, 'SNGLSETH': 0, 'BQXBTC': 0, 'BQXETH': 0, 'KNCBTC': 0, 'KNCETH': 0, 'FUNBTC': 0, 'FUNETH': 0, 'SNMBTC': 0, 'SNMETH': 0, 'NEOETH': 0, 'IOTABTC': 0, 'IOTAETH': 0, 'LINKBTC': 0, 'LINKETH': 0, 'XVGBTC': 0, 'XVGETH': 0, 'SALTBTC': 0, 'SALTETH': 0, 'MDABTC': 0, 'MDAETH': 0, 'MTLBTC': 0, 'MTLETH': 0, 'SUBBTC': 0, 'SUBETH': 0, 'EOSBTC': 0, 'SNTBTC': 0, 'ETCETH': 0, 'ETCBTC': 0, 'MTHBTC': 0, 'MTHETH': 0, 'ENGBTC': 0, 'ENGETH': 0, 'DNTBTC': 0, 'ZECBTC': 0, 'ZECETH': 0, 'BNTBTC': 0, 'ASTBTC': 0, 'ASTETH': 0, 'DASHBTC': 0, 'DASHETH': 0, 'OAXBTC': 0, 'ICNBTC': 0, 'BTGBTC': 0, 'BTGETH': 0, 'EVXBTC': 0, 'EVXETH': 0, 'REQBTC': 0, 'REQETH': 0, 'VIBBTC': 0, 'VIBETH': 0, 'HSRETH': 0, 'TRXBTC': 0, 'TRXETH': 0, 'POWRBTC': 0, 'POWRETH': 0, 'ARKBTC': 0, 'ARKETH': 0, 'YOYOETH': 0, 'XRPBTC': 0, 'XRPETH': 0, 'MODBTC': 0, 'MODETH': 0, 'ENJBTC': 0, 'ENJETH': 0, 'STORJBTC': 0, 'STORJETH': 0, 'BNBUSDT': 0, 'VENBNB': 0, 'YOYOBNB': 0, 'POWRBNB': 0, 'VENBTC': 0, 'VENETH': 0, 'KMDBTC': 0, 'KMDETH': 0, 'NULSBNB': 0, 'RCNBTC': 0, 'RCNETH': 0, 'RCNBNB': 0, 'NULSBTC': 0, 'NULSETH': 0, 'RDNBTC': 0, 'RDNETH': 0, 'RDNBNB': 0, 'XMRBTC': 0, 'XMRETH': 0, 'DLTBNB': 0, 'WTCBNB': 0, 'DLTBTC': 0, 'DLTETH': 0, 'AMBBTC': 0, 'AMBETH': 0, 'AMBBNB': 0, 'BCCETH': 0, 'BCCUSDT': 0, 'BCCBNB': 0, 'BATBTC': 0, 'BATETH': 0, 'BATBNB': 0, 'BCPTBTC': 0, 'BCPTETH': 0, 'BCPTBNB': 0, 'ARNBTC': 0, 'ARNETH': 0, 'GVTBTC': 0, 'GVTETH': 0, 'CDTBTC': 0, 'CDTETH': 0, 'GXSBTC': 0, 'GXSETH': 0, 'NEOUSDT': 0, 'NEOBNB': 0, 'POEBTC': 0, 'POEETH': 0, 'QSPBTC': 0, 'QSPETH': 0, 'QSPBNB': 0, 'BTSBTC': 0, 'BTSETH': 0, 'BTSBNB': 0, 'XZCBTC': 0, 'XZCETH': 0, 'XZCBNB': 0, 'LSKBTC': 0, 'LSKETH': 0, 'LSKBNB': 0, 'TNTBTC': 0, 'TNTETH': 0, 'FUELBTC': 0, 'FUELETH': 0, 'MANABTC': 0, 'MANAETH': 0, 'BCDBTC': 0, 'BCDETH': 0, 'DGDBTC': 0, 'DGDETH': 0, 'IOTABNB': 0, 'ADXBTC': 0, 'ADXETH': 0, 'ADXBNB': 0, 'ADABTC': 0, 'ADAETH': 0, 'PPTBTC': 0, 'PPTETH': 0, 'CMTBTC': 0, 'CMTETH': 0, 'CMTBNB': 0, 'XLMBTC': 0, 'XLMETH': 0, 'XLMBNB': 0, 'CNDBTC': 0, 'CNDETH': 0, 'CNDBNB': 0, 'LENDBTC': 0, 'LENDETH': 0, 'WABIBTC': 0, 'WABIETH': 0, 'WABIBNB': 0, 'LTCETH': 0, 'LTCUSDT': 0, 'LTCBNB': 0, 'TNBBTC': 0, 'TNBETH': 0, 'WAVESBTC': 0, 'WAVESETH': 0, 'WAVESBNB': 0, 'GTOBTC': 0, 'GTOETH': 0, 'GTOBNB': 0, 'ICXBTC': 0, 'ICXETH': 0, 'ICXBNB': 0, 'OSTBTC': 0, 'OSTETH': 0, 'OSTBNB': 0, 'ELFBTC': 0, 'ELFETH': 0, 'AIONBTC': 0, 'AIONETH': 0, 'AIONBNB': 0, 'NEBLBTC': 0, 'NEBLETH': 0, 'NEBLBNB': 0, 'BRDBTC': 0, 'BRDETH': 0, 'BRDBNB': 0, 'MCOBNB': 0, 'EDOBTC': 0, 'EDOETH': 0, 'WINGSBTC': 0, 'WINGSETH': 0, 'NAVBTC': 0, 'NAVETH': 0, 'NAVBNB': 0, 'LUNBTC': 0, 'LUNETH': 0, 'TRIGBTC': 0, 'TRIGETH': 0, 'TRIGBNB': 0, 'APPCBTC': 0, 'APPCETH': 0, 'APPCBNB': 0, 'VIBEBTC': 0, 'VIBEETH': 0, 'RLCBTC': 0, 'RLCETH': 0, 'RLCBNB': 0, 'INSBTC': 0, 'INSETH': 0, 'PIVXBTC': 0, 'PIVXETH': 0, 'PIVXBNB': 0, 'IOSTBTC': 0, 'IOSTETH': 0, 'CHATBTC': 0, 'CHATETH': 0, 'STEEMBTC': 0, 'STEEMETH': 0, 'STEEMBNB': 0, 'NANOBTC': 0, 'NANOETH': 0, 'NANOBNB': 0, 'VIABTC': 0, 'VIAETH': 0, 'VIABNB': 0, 'BLZBTC': 0, 'BLZETH': 0, 'BLZBNB': 0, 'AEBTC': 0, 'AEETH': 0, 'AEBNB': 0, 'RPXBTC': 0, 'RPXETH': 0, 'RPXBNB': 0, 'NCASHBTC': 0, 'NCASHETH': 0, 'NCASHBNB': 0, 'POABTC': 0, 'POAETH': 0, 'POABNB': 0, 'ZILBTC': 0, 'ZILETH': 0, 'ZILBNB': 0, 'ONTBTC': 0, 'ONTETH': 0, 'ONTBNB': 0, 'STORMBTC': 0, 'STORMETH': 0, 'STORMBNB': 0, 'QTUMBNB': 0, 'QTUMUSDT': 0, 'XEMBTC': 0, 'XEMETH': 0, 'XEMBNB': 0, 'WANBTC': 0, 'WANETH': 0, 'WANBNB': 0, 'WPRBTC': 0, 'WPRETH': 0, 'QLCBTC': 0, 'QLCETH': 0, 'SYSBTC': 0, 'SYSETH': 0, 'SYSBNB': 0, 'QLCBNB': 0, 'GRSBTC': 0, 'GRSETH': 0, 'ADAUSDT': 0, 'ADABNB': 0, 'CLOAKBTC': 0, 'CLOAKETH': 0}, "price_now" : {'ETHBTC': 0, 'LTCBTC': 0, 'BNBBTC': 0, 'NEOBTC': 0, 'QTUMETH': 0, 'EOSETH': 0, 'SNTETH': 0, 'BNTETH': 0, 'BCCBTC': 0, 'GASBTC': 0, 'BNBETH': 0, 'BTCUSDT': 0, 'ETHUSDT': 0, 'HSRBTC': 0, 'OAXETH': 0, 'DNTETH': 0, 'MCOETH': 0, 'ICNETH': 0, 'MCOBTC': 0, 'WTCBTC': 0, 'WTCETH': 0, 'LRCBTC': 0, 'LRCETH': 0, 'QTUMBTC': 0, 'YOYOBTC': 0, 'OMGBTC': 0, 'OMGETH': 0, 'ZRXBTC': 0, 'ZRXETH': 0, 'STRATBTC': 0, 'STRATETH': 0, 'SNGLSBTC': 0, 'SNGLSETH': 0, 'BQXBTC': 0, 'BQXETH': 0, 'KNCBTC': 0, 'KNCETH': 0, 'FUNBTC': 0, 'FUNETH': 0, 'SNMBTC': 0, 'SNMETH': 0, 'NEOETH': 0, 'IOTABTC': 0, 'IOTAETH': 0, 'LINKBTC': 0, 'LINKETH': 0, 'XVGBTC': 0, 'XVGETH': 0, 'SALTBTC': 0, 'SALTETH': 0, 'MDABTC': 0, 'MDAETH': 0, 'MTLBTC': 0, 'MTLETH': 0, 'SUBBTC': 0, 'SUBETH': 0, 'EOSBTC': 0, 'SNTBTC': 0, 'ETCETH': 0, 'ETCBTC': 0, 'MTHBTC': 0, 'MTHETH': 0, 'ENGBTC': 0, 'ENGETH': 0, 'DNTBTC': 0, 'ZECBTC': 0, 'ZECETH': 0, 'BNTBTC': 0, 'ASTBTC': 0, 'ASTETH': 0, 'DASHBTC': 0, 'DASHETH': 0, 'OAXBTC': 0, 'ICNBTC': 0, 'BTGBTC': 0, 'BTGETH': 0, 'EVXBTC': 0, 'EVXETH': 0, 'REQBTC': 0, 'REQETH': 0, 'VIBBTC': 0, 'VIBETH': 0, 'HSRETH': 0, 'TRXBTC': 0, 'TRXETH': 0, 'POWRBTC': 0, 'POWRETH': 0, 'ARKBTC': 0, 'ARKETH': 0, 'YOYOETH': 0, 'XRPBTC': 0, 'XRPETH': 0, 'MODBTC': 0, 'MODETH': 0, 'ENJBTC': 0, 'ENJETH': 0, 'STORJBTC': 0, 'STORJETH': 0, 'BNBUSDT': 0, 'VENBNB': 0, 'YOYOBNB': 0, 'POWRBNB': 0, 'VENBTC': 0, 'VENETH': 0, 'KMDBTC': 0, 'KMDETH': 0, 'NULSBNB': 0, 'RCNBTC': 0, 'RCNETH': 0, 'RCNBNB': 0, 'NULSBTC': 0, 'NULSETH': 0, 'RDNBTC': 0, 'RDNETH': 0, 'RDNBNB': 0, 'XMRBTC': 0, 'XMRETH': 0, 'DLTBNB': 0, 'WTCBNB': 0, 'DLTBTC': 0, 'DLTETH': 0, 'AMBBTC': 0, 'AMBETH': 0, 'AMBBNB': 0, 'BCCETH': 0, 'BCCUSDT': 0, 'BCCBNB': 0, 'BATBTC': 0, 'BATETH': 0, 'BATBNB': 0, 'BCPTBTC': 0, 'BCPTETH': 0, 'BCPTBNB': 0, 'ARNBTC': 0, 'ARNETH': 0, 'GVTBTC': 0, 'GVTETH': 0, 'CDTBTC': 0, 'CDTETH': 0, 'GXSBTC': 0, 'GXSETH': 0, 'NEOUSDT': 0, 'NEOBNB': 0, 'POEBTC': 0, 'POEETH': 0, 'QSPBTC': 0, 'QSPETH': 0, 'QSPBNB': 0, 'BTSBTC': 0, 'BTSETH': 0, 'BTSBNB': 0, 'XZCBTC': 0, 'XZCETH': 0, 'XZCBNB': 0, 'LSKBTC': 0, 'LSKETH': 0, 'LSKBNB': 0, 'TNTBTC': 0, 'TNTETH': 0, 'FUELBTC': 0, 'FUELETH': 0, 'MANABTC': 0, 'MANAETH': 0, 'BCDBTC': 0, 'BCDETH': 0, 'DGDBTC': 0, 'DGDETH': 0, 'IOTABNB': 0, 'ADXBTC': 0, 'ADXETH': 0, 'ADXBNB': 0, 'ADABTC': 0, 'ADAETH': 0, 'PPTBTC': 0, 'PPTETH': 0, 'CMTBTC': 0, 'CMTETH': 0, 'CMTBNB': 0, 'XLMBTC': 0, 'XLMETH': 0, 'XLMBNB': 0, 'CNDBTC': 0, 'CNDETH': 0, 'CNDBNB': 0, 'LENDBTC': 0, 'LENDETH': 0, 'WABIBTC': 0, 'WABIETH': 0, 'WABIBNB': 0, 'LTCETH': 0, 'LTCUSDT': 0, 'LTCBNB': 0, 'TNBBTC': 0, 'TNBETH': 0, 'WAVESBTC': 0, 'WAVESETH': 0, 'WAVESBNB': 0, 'GTOBTC': 0, 'GTOETH': 0, 'GTOBNB': 0, 'ICXBTC': 0, 'ICXETH': 0, 'ICXBNB': 0, 'OSTBTC': 0, 'OSTETH': 0, 'OSTBNB': 0, 'ELFBTC': 0, 'ELFETH': 0, 'AIONBTC': 0, 'AIONETH': 0, 'AIONBNB': 0, 'NEBLBTC': 0, 'NEBLETH': 0, 'NEBLBNB': 0, 'BRDBTC': 0, 'BRDETH': 0, 'BRDBNB': 0, 'MCOBNB': 0, 'EDOBTC': 0, 'EDOETH': 0, 'WINGSBTC': 0, 'WINGSETH': 0, 'NAVBTC': 0, 'NAVETH': 0, 'NAVBNB': 0, 'LUNBTC': 0, 'LUNETH': 0, 'TRIGBTC': 0, 'TRIGETH': 0, 'TRIGBNB': 0, 'APPCBTC': 0, 'APPCETH': 0, 'APPCBNB': 0, 'VIBEBTC': 0, 'VIBEETH': 0, 'RLCBTC': 0, 'RLCETH': 0, 'RLCBNB': 0, 'INSBTC': 0, 'INSETH': 0, 'PIVXBTC': 0, 'PIVXETH': 0, 'PIVXBNB': 0, 'IOSTBTC': 0, 'IOSTETH': 0, 'CHATBTC': 0, 'CHATETH': 0, 'STEEMBTC': 0, 'STEEMETH': 0, 'STEEMBNB': 0, 'NANOBTC': 0, 'NANOETH': 0, 'NANOBNB': 0, 'VIABTC': 0, 'VIAETH': 0, 'VIABNB': 0, 'BLZBTC': 0, 'BLZETH': 0, 'BLZBNB': 0, 'AEBTC': 0, 'AEETH': 0, 'AEBNB': 0, 'RPXBTC': 0, 'RPXETH': 0, 'RPXBNB': 0, 'NCASHBTC': 0, 'NCASHETH': 0, 'NCASHBNB': 0, 'POABTC': 0, 'POAETH': 0, 'POABNB': 0, 'ZILBTC': 0, 'ZILETH': 0, 'ZILBNB': 0, 'ONTBTC': 0, 'ONTETH': 0, 'ONTBNB': 0, 'STORMBTC': 0, 'STORMETH': 0, 'STORMBNB': 0, 'QTUMBNB': 0, 'QTUMUSDT': 0, 'XEMBTC': 0, 'XEMETH': 0, 'XEMBNB': 0, 'WANBTC': 0, 'WANETH': 0, 'WANBNB': 0, 'WPRBTC': 0, 'WPRETH': 0, 'QLCBTC': 0, 'QLCETH': 0, 'SYSBTC': 0, 'SYSETH': 0, 'SYSBNB': 0, 'QLCBNB': 0, 'GRSBTC': 0, 'GRSETH': 0, 'ADAUSDT': 0, 'ADABNB': 0, 'CLOAKBTC': 0, 'CLOAKETH': 0}, "percent": {'ETHBTC': 0, 'LTCBTC': 0, 'BNBBTC': 0, 'NEOBTC': 0, 'QTUMETH': 0, 'EOSETH': 0, 'SNTETH': 0, 'BNTETH': 0, 'BCCBTC': 0, 'GASBTC': 0, 'BNBETH': 0, 'BTCUSDT': 0, 'ETHUSDT': 0, 'HSRBTC': 0, 'OAXETH': 0, 'DNTETH': 0, 'MCOETH': 0, 'ICNETH': 0, 'MCOBTC': 0, 'WTCBTC': 0, 'WTCETH': 0, 'LRCBTC': 0, 'LRCETH': 0, 'QTUMBTC': 0, 'YOYOBTC': 0, 'OMGBTC': 0, 'OMGETH': 0, 'ZRXBTC': 0, 'ZRXETH': 0, 'STRATBTC': 0, 'STRATETH': 0, 'SNGLSBTC': 0, 'SNGLSETH': 0, 'BQXBTC': 0, 'BQXETH': 0, 'KNCBTC': 0, 'KNCETH': 0, 'FUNBTC': 0, 'FUNETH': 0, 'SNMBTC': 0, 'SNMETH': 0, 'NEOETH': 0, 'IOTABTC': 0, 'IOTAETH': 0, 'LINKBTC': 0, 'LINKETH': 0, 'XVGBTC': 0, 'XVGETH': 0, 'SALTBTC': 0, 'SALTETH': 0, 'MDABTC': 0, 'MDAETH': 0, 'MTLBTC': 0, 'MTLETH': 0, 'SUBBTC': 0, 'SUBETH': 0, 'EOSBTC': 0, 'SNTBTC': 0, 'ETCETH': 0, 'ETCBTC': 0, 'MTHBTC': 0, 'MTHETH': 0, 'ENGBTC': 0, 'ENGETH': 0, 'DNTBTC': 0, 'ZECBTC': 0, 'ZECETH': 0, 'BNTBTC': 0, 'ASTBTC': 0, 'ASTETH': 0, 'DASHBTC': 0, 'DASHETH': 0, 'OAXBTC': 0, 'ICNBTC': 0, 'BTGBTC': 0, 'BTGETH': 0, 'EVXBTC': 0, 'EVXETH': 0, 'REQBTC': 0, 'REQETH': 0, 'VIBBTC': 0, 'VIBETH': 0, 'HSRETH': 0, 'TRXBTC': 0, 'TRXETH': 0, 'POWRBTC': 0, 'POWRETH': 0, 'ARKBTC': 0, 'ARKETH': 0, 'YOYOETH': 0, 'XRPBTC': 0, 'XRPETH': 0, 'MODBTC': 0, 'MODETH': 0, 'ENJBTC': 0, 'ENJETH': 0, 'STORJBTC': 0, 'STORJETH': 0, 'BNBUSDT': 0, 'VENBNB': 0, 'YOYOBNB': 0, 'POWRBNB': 0, 'VENBTC': 0, 'VENETH': 0, 'KMDBTC': 0, 'KMDETH': 0, 'NULSBNB': 0, 'RCNBTC': 0, 'RCNETH': 0, 'RCNBNB': 0, 'NULSBTC': 0, 'NULSETH': 0, 'RDNBTC': 0, 'RDNETH': 0, 'RDNBNB': 0, 'XMRBTC': 0, 'XMRETH': 0, 'DLTBNB': 0, 'WTCBNB': 0, 'DLTBTC': 0, 'DLTETH': 0, 'AMBBTC': 0, 'AMBETH': 0, 'AMBBNB': 0, 'BCCETH': 0, 'BCCUSDT': 0, 'BCCBNB': 0, 'BATBTC': 0, 'BATETH': 0, 'BATBNB': 0, 'BCPTBTC': 0, 'BCPTETH': 0, 'BCPTBNB': 0, 'ARNBTC': 0, 'ARNETH': 0, 'GVTBTC': 0, 'GVTETH': 0, 'CDTBTC': 0, 'CDTETH': 0, 'GXSBTC': 0, 'GXSETH': 0, 'NEOUSDT': 0, 'NEOBNB': 0, 'POEBTC': 0, 'POEETH': 0, 'QSPBTC': 0, 'QSPETH': 0, 'QSPBNB': 0, 'BTSBTC': 0, 'BTSETH': 0, 'BTSBNB': 0, 'XZCBTC': 0, 'XZCETH': 0, 'XZCBNB': 0, 'LSKBTC': 0, 'LSKETH': 0, 'LSKBNB': 0, 'TNTBTC': 0, 'TNTETH': 0, 'FUELBTC': 0, 'FUELETH': 0, 'MANABTC': 0, 'MANAETH': 0, 'BCDBTC': 0, 'BCDETH': 0, 'DGDBTC': 0, 'DGDETH': 0, 'IOTABNB': 0, 'ADXBTC': 0, 'ADXETH': 0, 'ADXBNB': 0, 'ADABTC': 0, 'ADAETH': 0, 'PPTBTC': 0, 'PPTETH': 0, 'CMTBTC': 0, 'CMTETH': 0, 'CMTBNB': 0, 'XLMBTC': 0, 'XLMETH': 0, 'XLMBNB': 0, 'CNDBTC': 0, 'CNDETH': 0, 'CNDBNB': 0, 'LENDBTC': 0, 'LENDETH': 0, 'WABIBTC': 0, 'WABIETH': 0, 'WABIBNB': 0, 'LTCETH': 0, 'LTCUSDT': 0, 'LTCBNB': 0, 'TNBBTC': 0, 'TNBETH': 0, 'WAVESBTC': 0, 'WAVESETH': 0, 'WAVESBNB': 0, 'GTOBTC': 0, 'GTOETH': 0, 'GTOBNB': 0, 'ICXBTC': 0, 'ICXETH': 0, 'ICXBNB': 0, 'OSTBTC': 0, 'OSTETH': 0, 'OSTBNB': 0, 'ELFBTC': 0, 'ELFETH': 0, 'AIONBTC': 0, 'AIONETH': 0, 'AIONBNB': 0, 'NEBLBTC': 0, 'NEBLETH': 0, 'NEBLBNB': 0, 'BRDBTC': 0, 'BRDETH': 0, 'BRDBNB': 0, 'MCOBNB': 0, 'EDOBTC': 0, 'EDOETH': 0, 'WINGSBTC': 0, 'WINGSETH': 0, 'NAVBTC': 0, 'NAVETH': 0, 'NAVBNB': 0, 'LUNBTC': 0, 'LUNETH': 0, 'TRIGBTC': 0, 'TRIGETH': 0, 'TRIGBNB': 0, 'APPCBTC': 0, 'APPCETH': 0, 'APPCBNB': 0, 'VIBEBTC': 0, 'VIBEETH': 0, 'RLCBTC': 0, 'RLCETH': 0, 'RLCBNB': 0, 'INSBTC': 0, 'INSETH': 0, 'PIVXBTC': 0, 'PIVXETH': 0, 'PIVXBNB': 0, 'IOSTBTC': 0, 'IOSTETH': 0, 'CHATBTC': 0, 'CHATETH': 0, 'STEEMBTC': 0, 'STEEMETH': 0, 'STEEMBNB': 0, 'NANOBTC': 0, 'NANOETH': 0, 'NANOBNB': 0, 'VIABTC': 0, 'VIAETH': 0, 'VIABNB': 0, 'BLZBTC': 0, 'BLZETH': 0, 'BLZBNB': 0, 'AEBTC': 0, 'AEETH': 0, 'AEBNB': 0, 'RPXBTC': 0, 'RPXETH': 0, 'RPXBNB': 0, 'NCASHBTC': 0, 'NCASHETH': 0, 'NCASHBNB': 0, 'POABTC': 0, 'POAETH': 0, 'POABNB': 0, 'ZILBTC': 0, 'ZILETH': 0, 'ZILBNB': 0, 'ONTBTC': 0, 'ONTETH': 0, 'ONTBNB': 0, 'STORMBTC': 0, 'STORMETH': 0, 'STORMBNB': 0, 'QTUMBNB': 0, 'QTUMUSDT': 0, 'XEMBTC': 0, 'XEMETH': 0, 'XEMBNB': 0, 'WANBTC': 0, 'WANETH': 0, 'WANBNB': 0, 'WPRBTC': 0, 'WPRETH': 0, 'QLCBTC': 0, 'QLCETH': 0, 'SYSBTC': 0, 'SYSETH': 0, 'SYSBNB': 0, 'QLCBNB': 0, 'GRSBTC': 0, 'GRSETH': 0, 'ADAUSDT': 0, 'ADABNB': 0, 'CLOAKBTC': 0, 'CLOAKETH': 0}, "trades": []}, outfile)
	t1 = Process(target= main_loop)
	t1.start()
	bot.polling()