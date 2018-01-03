import json
import requests
import urllib3
import scraper
from flask import Flask, render_template
import telepot
import os

greetings = ["hi","hello","hey", "heyy", "heya"]

bot = telepot.Bot('389435360:AAFYKaUvs7iMgWCTcwAWwznJG_URoyPABkc')
print(bot.getMe())


app = Flask(__name__)

@app.route("/")
def handle(msg):        # Glance a message
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == "text":
        message = msg["text"].lower()

        # Main Structure

        if message == "/start":
            bot.sendMessage(chat_id, "Welcome to Crypto Bot where you will get all the details about the cryptocurrency market.")
        elif message in greetings:
            bot.sendMessage(chat_id, "Hi")
        elif "/checkprice" in message:
            message  = message.split(" ")
            coin = message[1].upper()
            price = scraper.get_current_price(coin)
            price = str(price[coin]["USD"])
            response = "*Details*" + "\n" + "Currency : " + coin + "\n" + "Current price : " + "$ " + price
            bot.sendMessage(chat_id, response, parse_mode='Markdown')
        elif message == "/topcryptos":
            top_10_currencies = scraper.get_top_10_currencies()
            response = "*Top 10 cryptocurrencies by market cap : *"
            for coin in top_10_currencies:
                index = str(top_10_currencies.index(coin) + 1)
                response = response + "\n" + index + ". " + coin
            bot.sendMessage(chat_id, response, parse_mode='Markdown')
        elif message == "/topexchanges":
            top_10_exchanges = scraper.get_top_10_exchanges()
            response = "*Top 10 cryptocurrency exchanges by volume : *"
            for exchange in top_10_exchanges:
                index = str(top_10_exchanges.index(exchange) + 1)
                response = response + "\n" + index + ". " + exchange
            bot.sendMessage(chat_id, response, parse_mode='Markdown')
        elif message == "/latestnews":
            latest_news = scraper.get_latest_crypto_news()
            bot.sendMessage(chat_id, "*Latest Cryptocurrency news : *", parse_mode="Markdown")
            for news in latest_news:
                headline = news["headlines"]
                link = news["link"]
                bot.sendMessage(chat_id, headline + "\n" + link)
        elif message == "/mostprofitable":
            most_profitable_by_year = {'coin':'', 'diff':-1}
            most_profitable_by_month = {'coin':'', 'diff':-1}
            most_profitable_by_day = {'coin':'', 'diff':-1}

            coins = scraper.get_codes_coins()

            for key in coins.keys():
                prices_diff = scraper.get_prices(int(coins[key]), "USD")
                if prices_diff['day'] > most_profitable_by_day['diff']:
                    most_profitable_by_day['diff'] = prices_diff['day']
                    most_profitable_by_day['coin'] = key

                if prices_diff['month'] > most_profitable_by_month['diff']:
                    most_profitable_by_month['diff'] = prices_diff['month']
                    most_profitable_by_month['coin'] = key

                if prices_diff['year'] > most_profitable_by_year['diff']:
                    most_profitable_by_year['diff'] = prices_diff['year']
                    most_profitable_by_year['coin'] = key

            response = "*Most Profitable*"
            response += "\n*By Day : *" + "*" + most_profitable_by_day['coin'] + "*" + "\n" + "Percentage : " + str(round(most_profitable_by_day['diff'],2)) + "%"
            response += "\n*By Month : *" + "*" + most_profitable_by_month['coin'] + "*" + "\n" + "Percentage : " + str(round(most_profitable_by_month['diff'],2)) + "%"
            response += "\n*By Year : *" + "*" + most_profitable_by_year['coin'] + "*" + "\n" + "Percentage : " + str(round(most_profitable_by_year['diff'],2)) + "%"
            bot.sendMessage(chat_id, response, parse_mode='Markdown')
        else:
            response = "Hey, I am still learning ! Kindly bear with me !"
            bot.sendMessage(chat_id, response, parse_mode='Markdown')


bot.message_loop(handle)

# # Keep the program running.
# while 1:
#     time.sleep(10)

def build_keyboard():

    keyboard = [[]]

    for i in range(len(coins)):
        keyboard[0].append(coins[i])

    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)
