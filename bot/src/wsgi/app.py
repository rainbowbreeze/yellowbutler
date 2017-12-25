#!flask/bin/python

"""
Conventions:
 Base APIs are exposed using the address https://_hostname_/yellowbutler/api/v1.0/

 Authorization code is passed in the X-Authorization field of the payload (or headers)

 Basic code to deal with Telegram: https://blog.pythonanywhere.com/148/
"""

from flask import Flask, request
from yellowbot.yellowbot import YellowBot
from yellowbot.botsurfacetelegram import BotSurfaceTelegram
# Telegram management
import telepot
import urllib3

# Basic address for all the API calls
BASIC_ADDRESS = '/yellowbot/api/v1.0'


# You can leave this bit out if you're using a paid PythonAnywhere account
proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))
# end of the stuff that's only needed for free accounts

telegram_bot = telepot.Bot('YOUR_AUTHORIZATION_TOKEN')
app = Flask(__name__)
yb = YellowBot()
bot_surface_telegram = BotSurfaceTelegram()


@app.route("/")
def hello_world():
    return 'Hello World!'


@app.route('{}/message'.format(BASIC_ADDRESS), methods=['POST'])
def echo_message():
    print('***************************')
    print(request.headers)
    print('***************************')
    print(request)
    print('***************************')
    print(request.get_json())
    print('***************************')


@app.route('{}/intent'.format(BASIC_ADDRESS), methods=['POST'])
def process_intent():
    """
    Process and intent with given parameters
    intent name is

    :return:
    """
    # return yb.process_intent("kindergarten_check", "bella storia")
    return yb.process_intent("kindergarten_check", "bella storia")


@app.route('/yellowbot/telegramwebhook/v1.0', methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        text = update["message"]["text"]
        chat_id = update["message"]["chat"]["id"]
        chat_response = bot_surface_telegram.process_chat_message(text)
        telegram_bot.sendMessage(chat_id, "From the web: you said '{}'".format(chat_response))
    return "OK"


if __name__ == '__main__':
    app.run(debug=True)
