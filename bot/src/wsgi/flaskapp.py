#!flask/bin/python

"""
Conventions:
 Base APIs are exposed using the address https://_hostname_/yellowbutler/api/v1.0/

 Authorization code in the request is passed in the X-Authorization field
  in headers
 If the client is not authorizes, an HTTP 401 status code is returned

 When an error is returned, the response body is a json, with the error
  status code 400 and the message field with explanation of the error code

Basic code to deal with Telegram: https://blog.pythonanywhere.com/148/


Useful links:
 A way to forge custom about responses for the abort method
  http://flask.pocoo.org/docs/0.12/api/#flask.Flask.make_response

  from flask import Flask, request, make_response, jsonify
   abort(
      make_response(
          jsonify(message="Message goes here"),
          402,
          {'X-Parachutes-header': 'parachutes are cool'}
      )
  )

 Another resource

"""

from flask import Flask, request, make_response, jsonify
from werkzeug.exceptions import abort, BadRequest

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
    print("Is json? {}".format(request.is_json))
    # print(request.get_json())  # Can create errors if the request is not properly json made
    print('******** END REQ *******************')
    print()

    # Request object format reference can be found at
    #  http://flask.pocoo.org/docs/0.12/api/#incoming-request-data

    # Find the authorization key
    auth_key = request.headers.get("X-Authorization")

    # None or invalid auth key
    if not yb.is_client_authorized(auth_key):
        abort(401)  # As per https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#4xx_Client_errors

    # Extract the intent from the request
    if not request.is_json:
        abort(make_response(
            jsonify(message="No json data in the request"), 400)
        )
    # This conversion can fail if content_type is set to application/json
    #  but body is empty, so it needs to be handled in the proper way
    #  Method reference is here: http://flask.pocoo.org/docs/0.12/api/#flask.Request.get_json
    try:
        # silent=True doesn't raise any error
        json_payload = request.get_json()
    except BadRequest as e:
        abort(make_response(
            jsonify(message="Invalid json body, cannot parse it"), 400)
        )
    if "intent" not in json_payload:
        abort(make_response(
            jsonify(message="Missing intent field in the request"), 400)
        )
    intent = request.json["intent"]
    # Extract the parameters from the request
    if "params" in request.json:
        params = request.json["params"]
    else:
        params = {}

    # Pass everything to the bot
    try:
        message = yb.process_intent(intent, params)  # Process the intent
        return make_response(jsonify(message=message), 200)
    except Exception as e:
        # If something goes wrong, like missing parameters or errors in
        #  the gear process, flow falls here
        abort(make_response(
            jsonify(message=e.args[0]), 400)
        )


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
