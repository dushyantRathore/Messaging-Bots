from bs4 import BeautifulSoup
import requests
import json
from cryptocompy import price

MAX_LIMIT = 10


def get_codes_coins():
	url = "https://cdn.api.coinranking.com/v1/public/coins"
	headers = {'User-Agent': 'Mozilla/5.0'}
	response = requests.get(url, headers)

	content = response.content.decode('utf-8')
	content = json.loads(content)

	coins = content['data']['coins'][:5]

	codes = {}

	for coin in coins:
		coin_name = coin['symbol']
		codes[coin_name] = coin['id']

	# print(codes)

	return codes



# Get the price of the currency

def get_current_price(coin):
	p = price.get_current_price(coin, "USD")
	return p[coin]["USD"]


# Get the top 10 cryptocurrencies

def get_top_10_currencies():
	url = "https://coinmarketcap.com/"
	headers = {'User-Agent': 'Mozilla/5.0'}
	response = requests.get(url, headers)
	soup = BeautifulSoup(response.text, "html.parser")

	top_10_currencies = []

	for a in soup.find_all("a", attrs={"class" : "currency-name-container"}):
		top_10_currencies.append(a.text)

	top_10_currencies = top_10_currencies[0:10]
	print(top_10_currencies)

	return top_10_currencies


# Get the top 10 cryptocurrency exchanges

def get_top_10_exchanges():
	url = "https://coinmarketcap.com/exchanges/volume/24-hour/"
	headers = {'User-Agent': 'Mozilla/5.0'}
	response = requests.get(url, headers)
	soup = BeautifulSoup(response.text, "html.parser")

	top_10_exchanges = []

	for h3 in soup.find_all("h3",attrs={"class" : "volume-header"}):
		for a in h3.find_all("a"):
			top_10_exchanges.append(a.text)

	top_10_exchanges = top_10_exchanges[0:10]
	print(top_10_exchanges)

	return top_10_exchanges


# Get the latest cryptocurrency news

def get_latest_crypto_news():
	url = "https://cryptoanswers.net/"
	headers = {'User-Agent': 'Mozilla/5.0'}
	response = requests.get(url, headers)
	soup = BeautifulSoup(response.text, "html.parser")

	crypto_news = soup.find('dl', attrs={'id':'ticker'})

	crypto_news = crypto_news.find_all('dd')

	trending_news = []

	for news in crypto_news:
		article = {"headlines": news.text, "link": news.a['href']}
		trending_news.append(article)
	print(trending_news)
	return trending_news


def get24hprice(code, comparison):
	url = "https://cdn.api.coinranking.com/v1/public/coin/"+str(code)+"/history/24h?base="+comparison
	headers = {'User-Agent': 'Mozilla/5.0'}
	response = requests.get(url, headers)

	content = response.content.decode('utf-8')
	content = json.loads(content)
	return float(content['data']['history'][0]['price']), float(content['data']['history'][-1]['price'])


def get1mprice(code, comparison):
	url = "https://cdn.api.coinranking.com/v1/public/coin/"+str(code)+"/history/1m?base="+comparison
	headers = {'User-Agent': 'Mozilla/5.0'}
	response = requests.get(url, headers)

	content = response.content.decode('utf-8')
	content = json.loads(content)
	return float(content['data']['history'][0]['price'])


def get1yprice(code, comparison):
	url = "https://cdn.api.coinranking.com/v1/public/coin/"+str(code)+"/history/1y?base="+comparison
	headers = {'User-Agent': 'Mozilla/5.0'}
	response = requests.get(url, headers)

	content = response.content.decode('utf-8')
	content = json.loads(content)
	return float(content['data']['history'][0]['price'])


def get_prices(code, comparison):
	# if currency == "BTC":
	# 	code = 1335
	# elif currency == "XRP":
	# 	code = 840
	# elif currency == "ETH":
	# 	code = 1211
	# elif currency == "LTC":
	# 	code = 527

	prices = {}

	prices['24h'], prices['current'] = get24hprice(code, comparison)
	prices['1m'] = get1mprice(code, comparison)
	prices['1y'] = get1yprice(code, comparison)
		
	# print(code, prices)

	prices_diff = {}

	if prices['24h'] == 0:
		prices_diff['day'] = 0
	else:
		prices_diff['day'] = ((prices['current']-prices['24h'])/prices['24h'])*100

	if prices['1m'] == 0:
		prices_diff['month'] = 0
	else:
		prices_diff['month'] = ((prices['current']-prices['1m'])/prices['1m'])*100

	if prices['1y'] == 0:
		prices_diff['year'] = 0
	else:
		prices_diff['year'] = ((prices['current']-prices['1y'])/prices['1y'])*100

	# print(prices_diff)

	return prices_diff

# def get_top_10_cryptocurrencies():
# 	url = "https://coinranking.com/"
# 	headers = {'User-Agent': 'Mozilla/5.0'}
# 	response = requests.get(url, headers)
#
# 	soup = BeautifulSoup(response.text, 'html.parser')
#
# 	currencies = soup.find_all('a', attrs={'class':'coin-list__body__row'})
#
# 	count = 0
# 	top_10_currencies = []
#
# 	for currency in currencies:
#
# 		currency_name = currency.find('span', attrs={'class':'coin-name'}).text
# 		top_10_currencies.append(currency_name)
#
# 		count = count + 1
#
# 		if count == MAX_LIMIT:
# 			break;
#
# 	print(top_10_currencies)
#
# 	return top_10_currencies


# def get_top_10_exchanges():
# 	url = "https://coinmarketcap.com/exchanges/volume/24-hour/all/"
# 	headers = {'User-Agent': 'Mozilla/5.0'}
# 	response = requests.get(url, headers)
#
# 	soup = BeautifulSoup(response.text, 'html.parser')
#
# 	exchanges = soup.find_all('td', attrs={'class':'volume-header-container'})
#
# 	top_10_exchanges = []
#
# 	count = 0
#
# 	for exchange in exchanges:
# 		exchange_detail = {}
# 		exchange_detail['name'] = exchange.find('a').text
#
# 		url = "https://coinmarketcap.com/exchanges/"+exchange_detail['name']
# 		headers = {'User-Agent': 'Mozilla/5.0'}
# 		response = requests.get(url, headers)
#
# 		soup = BeautifulSoup(response.text, 'html.parser')
#
# 		exchange_detail['link'] = soup.find('ul', attrs={'class':'list-unstyled'}).find('a').href
#
# 		top_10_exchanges.append(exchange_detail)
#
# 		count = count + 1
#
# 		if count == MAX_LIMIT:
#
# 			break
#
# 	print(top_10_exchanges)

#	return top_10_exchanges
