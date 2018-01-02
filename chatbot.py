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



bot.message_loop(handle)

# # Keep the program running.
# while 1:
#     time.sleep(10)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
