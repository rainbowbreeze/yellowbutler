#!flask/bin/python

"""
Conventions:
 Base APIs are exposed using the address https://_hostname_/yellowbutler/api/v1.0/

 Authorization code is passed in the X-Authorization field of the payload (or headers)

 Basic code to deal with Telegram: https://blog.pythonanywhere.com/148/
"""

from flask import Flask, request
from werkzeug.exceptions import abort

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
    return "Hello World!"


@app.route('{}/intent'.format(BASIC_ADDRESS), methods=['POST'])
def process_intent():
    """
    Process and intent with given parameters

    :return:
    """

    print('******** NEW REQ *******************')
    print(request.headers)
    print('***************************')
    print(request.data)
    print('***************************')
    print(request.is_json)
    print('***************************')
    #print(request.get_json(force=True))
    print(request.get_json())
    print('***************************')

    # Request object format reference can be found at
    #  http://flask.pocoo.org/docs/0.12/api/#incoming-request-data

    # Find the authorization key
    auth_key = request.headers.get("X-Authorization")

    if not yb.is_client_authorized(auth_key):
        abort(401)  # As per https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#4xx_Client_errors

    # Extract the intent from the request
    if not request.is_json:
        # TODO add the message for no json data
        abort(400)
    if "intent" not in request.json:
        # TODO add the need for the intent param
        abort(400)
    intent = request.json["intent"]
    # Extract the parameters from the request
    if "params" in request.json:
        params = request.json["params"]
    else:
        params = {}
    # TODO add the need for the params param

    # Pass everything to the bot
    try:
        return yb.process_intent(intent, params)
    except ValueError:
        # TODO put the ValueError exception as string for the abort
        abort(400)


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
