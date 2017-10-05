import telepot
import requests
import json
import os
from flask import Flask,jsonify,render_template

bot = telepot.Bot('386925653:AAE52ubyjvCWrxXQgySBmiowG8G8xyMm7g4')

# print(bot.getMe())

details = {}


app = Flask(__name__)


def get_location_details(lat,lon):

    header = {"user-key": "e5643d5519ea87a914cf5d44e806fa61"}
    Zomato_request_url = "https://developers.zomato.com/api/v2.1/geocode?lat=" + lat + "&lon=" + lon
    r = requests.post(Zomato_request_url, headers=header)
    res = json.loads(r.text)
    r.close()

    global details
    details = res

    return res


@app.route("/")
def handle(msg):        # Glance a message
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == "text":
        message = msg["text"].lower()

        # Main Structure

        if message == "/start":
            bot.sendMessage(chat_id, "Welcome to Resto Bot. Please send your location to proceed further : ")
        elif message in ["hi", "hey", "heya", "hello", "hey"]:
            bot.sendMessage(chat_id, "Hi")
        elif message in ["1.", "1)", "1"]:
            popularity = str(details["popularity"]["popularity"])
            nightlife_index = str(details["popularity"]["nightlife_index"])
            bot.sendMessage(chat_id, "Popularity : " + popularity + ""
                            "\nNightlife Index : " + nightlife_index)
        elif message in ["2.", "2)", "2"]:
            l = int(len(details["popularity"]["top_cuisines"]))

            text = "The top cuisines offered are : \n"
            for i in range(0,l):
                text += str(details["popularity"]["top_cuisines"][i])
                text += "\n"

            bot.sendMessage(chat_id, text)

        elif message in ["3.", "3)", "3"]:
            l = int(len(details["nearby_restaurants"]))
            bot.sendMessage(chat_id, "The following are the most popular restaurants in your area : ")

            for i in range(0,l):
                text = ""
                text += "\nName : " + str(details["nearby_restaurants"][i]["restaurant"]["name"])
                text += "\nURL : " + str(details["nearby_restaurants"][i]["restaurant"]["url"])
                text += "\nAddress : " + str(details["nearby_restaurants"][i]["restaurant"]["location"]["address"])
                text += "\nAverage cost for two : " + str(details["nearby_restaurants"][i]["restaurant"]["average_cost_for_two"])
                text += "\nRating : " + str(details["nearby_restaurants"][i]["restaurant"]["user_rating"]["aggregate_rating"])

                bot.sendMessage(chat_id, text)

    elif content_type == "location":
        lat = str(msg['location']['latitude'])
        lon = str(msg['location']['longitude'])

        res = get_location_details(lat, lon)

        location = res["location"]["title"]
        city = res["location"]["city_name"]
        country = res["location"]["country_name"]

        bot.sendMessage(chat_id, "Your current location is  : " + str(location) + ", " + str(city) + ", " + str(country) + "" \
                        "\n\nPlease choose your option : "
                        "\n1. Explore popularity and nightlife index"
                        "\n2. Explore top cuisines"
                        "\n3. Explore nearby restaurants")

        return "ok"


bot.message_loop(handle)

# # Keep the program running.
# while 1:
#     time.sleep(10)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)