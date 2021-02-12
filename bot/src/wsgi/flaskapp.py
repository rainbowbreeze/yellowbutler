#!flask/bin/python

"""
Conventions:
 Base APIs are exposed using the address https://_hostname_/yellowbutler/api/v1.0/

 This class shields the bot from unauthorized access. Based on the
  different ways the bot could be reached, different checks are performed
 When an API request is received, Authorization code has to be passed in the
  X-Authorization field in request headers
 When a Telegram request is received, user id is used as authorization code
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
import threading

from flask import Flask, request, make_response, jsonify
from werkzeug.exceptions import abort, BadRequest

from yellowbot.globalbag import GlobalBag
from yellowbot.loggingservice import LoggingService
from yellowbot.yellowbot import YellowBot
from yellowbot.surfaces.telegramsurface import TelegramSurface


# Init logging
LoggingService.init()
_logger = LoggingService.get_logger(__name__)

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


def receive_message_thread(yellowbot: YellowBot, message):
    """
    Thread function to send messages to YellowBot

    :param yellowbot:
    :type yellowbot: YellowBot

    :param message: the message to send
    :type message: SurfaceMessage
    """

    # The expectaion is that error handling happen inside this method
    #  so the try here is really for exceptional cases
    try:
        yellowbot.receive_message(message)
    except BaseException as err:
        _logger.exception("For some reasons, an error bubbled up in the receive_message: {}".format(err))


def tick_scheduler_thread(yellowbot: YellowBot):
    """
    Therad function to launch the scheduler service in YellowBot

    :param yellowbot:
    :type yellowbot: YellowBot
    """
    # The expectaion is that error handling happen inside this method
    #  so the try here is really for exceptional cases
    try:
        yellowbot.tick_scheduler()
    except BaseException as err:
        _logger.exception("For some reasons, an error bubbled up in the schedules: {}".format(err))


@app.route("/")
def home():
    return "YellowBot here, happy to serve at {} :)".format(
        FLASK_BASE_API_ADDRESS
    )


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

    _logger.info("API call for Intent arrived")

    # Find the authorization key
    auth_key = request.headers.get("X-Authorization")

    if not auth_key:
        _logger.warning("Unauthorized access registered with no key provided")
        abort(401)  # As per https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#4xx_Client_errors


    # None or invalid auth key
    if not yellowbot.is_client_authorized(auth_key):
        _logger.warning("Unauthorized access registered with key {}".format(auth_key))
        abort(403)  # As per https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#4xx_Client_errors

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

    _logger.info("Routing call for intent {}".format(intent))
    try:
        execution_result = yellowbot.process_intent(intent, params)  # Process the intent
        if execution_result.went_well():
            _logger.debug("Gear call returned: {}".format(execution_result.get_messages()))
            return make_response(
                jsonify(message=execution_result.get_messages()),
                200
            )
        else:
            _logger.debug("Error in gear call: {}".format(execution_result.get_messages()))
            return make_response(
                jsonify(
                    message=execution_result.get_plan_message(),
                    errorcode=execution_result.get_result()),
                400
            )
    except Exception as e:
        # If something goes wrong, like missing parameters or errors in
        #  the gear process, flow falls here
        _logger.warning("Error {} processing intent {}".format(
            e.__class__,
            e.args[0]
        ))
        abort(make_response(
            jsonify(message=e.args[0]), 400)
        )


@app.route('{}/scheduler'.format(FLASK_BASE_API_ADDRESS), methods=['GET'])
def process_scheduler():
    """
    Called by the App Engine job scheduler, triggers a check in the scheduler
    :return: The code should return an HTTP status code within the range
    200-299 to indicate success. Any other code indicates that the task failed.
    """
    _logger.info("API call for Scheduler arrived")

    # AppEngine special auth key?
    # See at https://cloud.google.com/appengine/docs/flexible/python/scheduling-jobs-with-cron-yaml
    #  section "Validating Cron Requests"
    auth_key = request.headers.get("X-Appengine-Cron")
    if not auth_key:
        # Find the authorization key using the usual way
        auth_key = request.headers.get("X-Authorization")
        # None or invalid auth key
        if not yellowbot.is_client_authorized(auth_key):
            abort(401)  # As per https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#4xx_Client_errors

    _logger.info("Routing call for scheduler")
    t = threading.Thread(
        name="Scheduler",
        target=tick_scheduler_thread,
        args=(yellowbot,))  # Final , is to disambiguate a tuple of parameters instead of a string
    t.start()
    return make_response("OK", 200)


@app.route(FLASK_TELEGRAM_BOT_LURCH_WEBHOOK, methods=["POST"])
def telegram_webhook_lurch():
    """
    Webhook for LurchBot on Telegram.
    Once the request is received, is routed to the YellowBot in a separate
     thread

    :return: 200 as status code and OK as message, regardless the
    result of the operation. Otherwise Telegram will keep sending
    the same message over and over
    """
    _logger.info("API call for Telegram Lurch bot arrived")

    update = request.get_json()

    # Checks if the message is authorized
    auth_key = TelegramSurface.from_telegram_update_to_auth_key(update)

    # None or invalid auth key
    if not yellowbot.is_client_authorized(auth_key):
        _logger.info("Notify admin about the unauthorized access from Telegram")
        # Send an alert message to admin channel
        try:
            yellowbot.notify_admin(
                "Invalid auth_key #{}# received from user {}-{}, with text ##{}##".format(
                    auth_key,
                    update["message"]["from"]["id"],
                    update["message"]["from"]["first_name"],
                    update["message"]["text"]
                )
            )
        except KeyError:
            # Any other error is re-raised after the finally clause has been executed
            # Look at https://docs.python.org/3.6/tutorial/errors.html#defining-clean-up-actions
            _logger.exception("Message from Telegram Lurch does not have the right fields\n {}".format(update))
        finally:
            # Send an 200, otherwise with 401 or other error codes Telegram
            #  keeps sending the message over and over. But in the data field
            #  of the response the message of unauthorized access is put
            # abort(401)  # As per https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#4xx_Client_errors
            return make_response("Not authorized", 200)

    else:
        _logger.info("Routing call for Telegram Lurch bot")
        # Extract the message from the Telegram update
        surface_message = TelegramSurface.from_telegram_update_to_message(
            GlobalBag.SURFACE_TELEGRAM_BOT_LURCH,
            update)
        # And process it on a separate thread
        t = threading.Thread(
            name="Intent",
            target=receive_message_thread,
            args=(yellowbot, surface_message))
        t.start()
        return make_response("OK", 200)


@app.errorhandler(500)
def server_error(err):
    """
    Manage uncaught exception

    For 500 error, see docs at http://flask.pocoo.org/docs/0.12/api/#flask.Flask.handle_exception
    """

    _logger.exception("An error occurred during a request: {}".format(err))
    return"""
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(err), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    #
    # For PythonAnywhere, please configure the WSGI file on the webapp
    #  as per quickstart tutorial
    app.run(debug=True)
