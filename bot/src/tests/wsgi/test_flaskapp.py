"""
Test the Flask app

How to test Flask: http://flask.pocoo.org/docs/0.12/testing/

For CL testing:
curl -X POST 127.0.0.1:5000/yellowbot/api/v1.0/intent -H "X-Authorization:authorized_key_1" -H "Content-Type: application/json" -d "{\"intent\":\"echo_message\", \"params\":{\"message\":\"Greetings from myself\"}}

To generate a proper json payload while making the request, both are mandatory:
  data=json.dumps(data)
  content_type="application/json"
  from: https://hairycode.org/2014/01/18/api-testing-with-flask-post/

Another clever way to manage json in the testing is here
 https://stackoverflow.com/questions/28836893/how-to-send-requests-with-jsons-in-unit-tests
 Basically, it adds json-skills to Flask BaseResponse and FlaskClient objects
  creating custom json fields, something they don't have because everything
  is manager using data field of BaseResponse, and content_type header
"""

from unittest import TestCase

from flask import json

from wsgi import flaskapp
from yellowbot.globalbag import GlobalBag

# Remember about the test environment setup in __init__.py file of this module


class TestFlaskApp(TestCase):
    def setUp(self):
        flaskapp.app.testing = True
        self.app = flaskapp.app.test_client()

    def tearDown(self):
        pass

    def test_rootUrl(self):
        response = self.app.get("/", follow_redirects=True)
        assert 200 == response.status_code
        assert b"YellowBot here, happy to serve at /yellowbot/api/v1.0 :)" in response.get_data()

    def test_authorizationForIntent(self):
        # Injects new auth keys
        flaskapp.yellowbot.change_authorized_keys(["auth_for_tests_1", "auth_for_tests_2"])

        data = {
            "intent": "test_intent",
            "params": {"test_param_1": "test_value_1"}
        }

        # No auth header at all
        response = self.app.post(
            "{}/intent".format(flaskapp.FLASK_BASE_API_ADDRESS),
            data=json.dumps(data), # Has to be dumped
            content_type="application/json", # Has to be specified
            follow_redirects=True
        )
        assert 401 == response.status_code

        # Not valid key passed in auth header
        response = self.app.post(
            "{}/intent".format(flaskapp.FLASK_BASE_API_ADDRESS),
            headers={"X-Authorization": "test_key_1"},
            data=json.dumps(data), # Has to be dumped
            content_type="application/json", # Has to be specified
            follow_redirects=True
        )
        assert 401 == response.status_code

        # Valid key passed in auth header
        response = self.app.post(
            "{}/intent".format(flaskapp.FLASK_BASE_API_ADDRESS),
            headers={"X-Authorization": "auth_for_tests_1"},
            data=json.dumps(data), # Has to be dumped
            content_type="application/json", # Has to be specified
            follow_redirects=True
        )
        assert 200 == response.status_code

        # Valid key passed in auth header
        response = self.app.post(
            "{}/intent".format(flaskapp.FLASK_BASE_API_ADDRESS),
            headers={"X-Authorization": "auth_for_tests_2"},
            data=json.dumps(data), # Has to be inside dumps
            content_type="application/json", # Has to be specified
            follow_redirects=True
        )
        assert 200 == response.status_code

    def test_authorizationForTelegram(self):
        # Injects new auth keys
        flaskapp.yellowbot.change_authorized_keys(["1234567890"])

        telegram_data = {
            'message': {
                'text': "Random message text",
                'chat': {
                    'id': 2312321
                },
                'from': {
                    'id': 123456,
                    'first_name': "User_First_Name"
                }
            }
        }

        # Not valid key passed in auth header
        response = self.app.post(
            flaskapp.FLASK_TELEGRAM_BOT_LURCH_WEBHOOK,
            data=json.dumps(telegram_data),  # Has to be dumped
            content_type="application/json",  # Has to be specified
            follow_redirects=True
        )
        assert 200 == response.status_code
        assert b"Not authorized" == response.data

        # Valid key passed in auth header
        telegram_data["message"]["from"]["id"] = 1234567890
        response = self.app.post(
            flaskapp.FLASK_TELEGRAM_BOT_LURCH_WEBHOOK,
            data=json.dumps(telegram_data), # Has to be dumped
            content_type="application/json", # Has to be specified
            follow_redirects=True
        )
        assert 200 == response.status_code
        assert b"OK" == response.data

    def test_BadAndGoodRequestsForIntent(self):
        # Injects new auth keys
        flaskapp.yellowbot.change_authorized_keys(["auth_for_tests_1"])

        # no json at all
        response = self.app.post(
            "{}/intent".format(flaskapp.FLASK_BASE_API_ADDRESS),
            headers={"X-Authorization": "auth_for_tests_1"},
            follow_redirects=True
        )
        assert 400 == response.status_code
        assert "application/json" == response.mimetype
        # print(response.get_data(as_text=True))
        assert b"message" in response.get_data()
        assert "No json data in the request" == json.loads(response.get_data())["message"]

        # Missing json, but content_type specified
        response = self.app.post(
            "{}/intent".format(flaskapp.FLASK_BASE_API_ADDRESS),
            headers={"X-Authorization": "auth_for_tests_1"},
            content_type="application/json",
            follow_redirects=True
        )
        assert 400 == response.status_code
        assert "application/json" == response.mimetype
        assert "Invalid json body, cannot parse it" == json.loads(response.get_data())["message"]

        # json is OK, but intent field is missing
        response = self.app.post(
            "{}/intent".format(flaskapp.FLASK_BASE_API_ADDRESS),
            headers={"X-Authorization": "auth_for_tests_1"},
            content_type="application/json",
            data=json.dumps({
                "intent_ZZZ": "test_intent",
            }),
            follow_redirects=True
        )
        assert 400 == response.status_code
        assert "application/json" == response.mimetype
        assert "Missing intent field in the request" == json.loads(response.get_data())["message"]

        # Only intent, but good because parameters are not required
        response = self.app.post(
            "{}/intent".format(flaskapp.FLASK_BASE_API_ADDRESS),
            headers={"X-Authorization": "auth_for_tests_1"},
            content_type="application/json",
            data=json.dumps({
                "intent": "test_intent"
            }),
            follow_redirects=True
        )
        assert 200 == response.status_code
        assert "application/json" == response.mimetype
        assert "No gear to process your intent" == json.loads(response.get_data())["message"]

        # Good intent, but lack of mandatory parameters
        data = {
            "intent": GlobalBag.ECHO_MESSAGE_INTENT,
        }
        response = self.app.post(
            "{}/intent".format(flaskapp.FLASK_BASE_API_ADDRESS),
            headers={"X-Authorization": "auth_for_tests_1"},
            data=json.dumps(data),
            content_type="application/json",
            follow_redirects=True
        )
        assert 200 == response.status_code
        assert "application/json" == response.mimetype
        assert "Missing message parameter in the request" == json.loads(response.get_data())["message"]

        # Good intent, but wrong parameters
        data = {
            "intent": GlobalBag.ECHO_MESSAGE_INTENT,
            "params": {"zzzz": "Good morning"}
        }
        response = self.app.post(
            "{}/intent".format(flaskapp.FLASK_BASE_API_ADDRESS),
            headers={"X-Authorization": "auth_for_tests_1"},
            data=json.dumps(data),
            content_type="application/json",
            follow_redirects=True
        )
        assert 200 == response.status_code
        assert "application/json" == response.mimetype
        assert "Missing message parameter in the request" == json.loads(response.get_data())["message"]

        # Finally, Good intent and good parameters
        data = {
            "intent": GlobalBag.ECHO_MESSAGE_INTENT,
            "params": {GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE: "Good morning"}
        }
        response = self.app.post(
            "{}/intent".format(flaskapp.FLASK_BASE_API_ADDRESS),
            headers={"X-Authorization": "auth_for_tests_1"},
            data=json.dumps(data),
            content_type="application/json",
            follow_redirects=True
        )
        assert 200 == response.status_code
        assert "application/json" == response.mimetype
        assert "Good morning" == json.loads(response.get_data())["message"]
