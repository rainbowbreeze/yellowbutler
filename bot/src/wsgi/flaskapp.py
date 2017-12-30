#!flask/bin/python

"""
Conventions:
 Base APIs are exposed using the address https://_hostname_/yellowbutler/api/v1.0/

 This class shields the bot from unauthorized access. Based on the
  different ways the bot could be reached, different checks are performed
 When an API request is received, Authorization code has to be passed in the
  X-Authorization field in request headers
 When a Telegram request is received, chat_id is used as authorization code
 If the client is not authorizes, an HTTP 401 status code is returned

 When an error is returned, the response has the error status code set to 400
  and the body is a json, with a message field with explanation of the error code

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

 Basic code to deal with Telegram: https://blog.pythonanywhere.com/148/
"""
import logging

from flask import Flask, request, make_response, jsonify
from werkzeug.exceptions import abort, BadRequest

from yellowbot.globalbag import GlobalBag
from yellowbot.surfaces.surfacemessage import SurfaceMessage
from yellowbot.yellowbot import YellowBot
from yellowbot.surfaces.telegramsurface import TelegramSurface


# Flask init
app = Flask(__name__)


# Allow to setup a test environment. It's dirty and I don't like it, but
#  it works.
# Used to avoid error like too many requests for Telegram webhook check etc
yellowbot = YellowBot(test_mode=GlobalBag.TEST_ENVIRONMENT)

# Base address for all the API calls
FLASK_BASE_API_ADDRESS = yellowbot.get_config("base_api_address")
FLASK_TELEGRAM_BOT_LURCH_WEBHOOK = yellowbot.get_config("telegram_lurch_webhook_url_relative")

# Logging to unix log utils
# See http://flask.pocoo.org/docs/0.10/errorhandling/#logging-to-a-file


class FlaskManager:
    """
    Class to gather all the flask routes as class's static methods. I like
     that more than defining them as global functions (the usual way you can
     find in tutorials)
    """

    @staticmethod
    @app.route("/")
    def hello_world():
        return "YellowBot here, happy to serve at {} :)".format(
            FLASK_BASE_API_ADDRESS
        )

    @staticmethod
    @app.route('{}/intent'.format(FLASK_BASE_API_ADDRESS), methods=['POST'])
    def process_intent():
        """
        Process and intent with given parameters

        :return:
        """

        # Request object format reference can be found at
        #  http://flask.pocoo.org/docs/0.12/api/#incoming-request-data

        # print('******** NEW REQ *******************')
        # print(request.headers)
        # print('***************************')
        # print(request.data)
        # print('***************************')
        # print("Is json? {}".format(request.is_json))
        # # print(request.get_json())  # Can create errors if the request is not properly json made
        # print('******** END REQ *******************')

        # Find the authorization key
        auth_key = request.headers.get("X-Authorization")

        # None or invalid auth key
        if not yellowbot.is_client_authorized(auth_key):
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
        except BadRequest:
            abort(make_response(
                jsonify(message="Invalid json body, cannot parse it"), 400)
            )
        # No intent field in the request
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
            message = yellowbot.process_intent(intent, params)  # Process the intent
            return make_response(jsonify(message=message), 200)
        except Exception as e:
            # If something goes wrong, like missing parameters or errors in
            #  the gear process, flow falls here
            abort(make_response(
                jsonify(message=e.args[0]), 400)
            )

    @staticmethod
    @app.route(FLASK_TELEGRAM_BOT_LURCH_WEBHOOK, methods=["POST"])
    def telegram_webhook():
        update = request.get_json()

        # Checks if the message is authorized
        auth_key = TelegramSurface.from_telegram_update_to_auth_key(update)
        # None or invalid auth key
        if not yellowbot.is_client_authorized(auth_key):
            yellowbot.send_message(SurfaceMessage(
                GlobalBag.SURFACE_TELEGRAM_BOT_LURCH,
                "185752881",
                "Invalid auth_key #{}# of type {} received from user {}-{}, with text ##{}##".format(
                    auth_key,
                    type(auth_key),
                    update["message"]["from"]["id"],
                    update["message"]["from"]["first_name"],
                    update["message"]["text"]
                )
            ))
            # abort(401)  # As per https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#4xx_Client_errors

        # Extract the message from the
        surface_message = TelegramSurface.from_telegram_update_to_message(
            GlobalBag.SURFACE_TELEGRAM_BOT_LURCH,
            update)
        yellowbot.receive_message(surface_message)
        return "OK"

    @staticmethod
    @app.errorhandler(500)
    def server_error(e):
        logging.exception('An error occurred during a request.')
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    #
    # For PythonAnywhere, please configure the WSGI file on the webapp
    #  as per quickstart tutorial
    app.run(debug=True)
