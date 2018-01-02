import json
import requests
import urllib2
import scraper

TOKEN = "389435360:AAFYKaUvs7iMgWCTcwAWwznJG_URoyPABkc"
URL = "http://api.telegram.org/bot{}".format(TOKEN)
TIME_OUT = 100

greetings = ["hi","hello","hey"]
coins = ["BTC","ETH","XRP","LTC"]

def get_chats(last_update_id):

    if last_update_id:
        response = requests.get(URL+"/getUpdates?timeout={}&offset={}".format(TIME_OUT, last_update_id))
    else:
        response = requests.get(URL+"/getUpdates?timeout={}&offset={}".format(TIME_OUT, last_update_id))

    content = response.content.decode("utf-8")
    content = json.loads(content)

    return content


def send_reply(chat_id, message):

    message = message.lower()

    reply_markup = None

    if message in greetings:
        reply = "Hey there !"
    elif message == "check price":
        reply_markup = build_keyboard()
        # print reply_markup
        reply = "Choose one"
    elif message == "/topcryptos":
        reply = scraper.get_top_10_cryptocurrencies()
        print reply
    else:
        reply = "Hey, I am still learning, kindly bear with me !"

    reply = urllib2.quote(reply)

    if reply_markup:
        requests.get(URL + "/sendMessage?chat_id={}&text={}&parse_mode=Markdown&reply_markup={}".format(chat_id, reply, reply_markup))
    else:
        requests.get(URL + "/sendMessage?chat_id={}&text={}".format(chat_id, reply))


def get_last_update_id(updates):

    update_ids = []

    for update in updates:
        update_ids.append(int(update["update_id"]))

    return max(update_ids)


def build_keyboard():

    keyboard = [[]]

    for i in range(len(coins)):
        keyboard[0].append(str(i+1))

    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def main():
    last_update_id = None

    while True:
        updates = get_chats(last_update_id)

        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates["result"]) + 1

            for update in updates["result"]:
                try:
                    message = update["message"]["text"]
                    chat_id = update["message"]["chat"]["id"]
                    send_reply(chat_id, message)
                except Exception as e:
                    print(e)


if __name__ == "__main__":
    main()
    # print json.loads(get_chats(None))["result"]
