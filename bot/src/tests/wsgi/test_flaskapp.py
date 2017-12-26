"""
Test the Flask app

How to test Flask: http://flask.pocoo.org/docs/0.12/testing/

For CL testing:
curl -X POST 127.0.0.1:5000/yellowbot/api/v1.0/intent -H "X-Authorization:authorized_key_1" -H "Content-Type: application/json" -d "{\"intent\":\"echo_message\", \"params\":{\"message\":\"Ciao da meeeeee\"}}

To generate a proper json payload while making the request, both are mandatory:
  data=json.dumps(data)
  content_type="application/json"
"""
from unittest import TestCase

from flask import json

from wsgi import flaskapp
from yellowbot.globalbag import GlobalBag


class TestFlaskApp(TestCase):
    def setUp(self):
        flaskapp.app.testing = True
        self.app = flaskapp.app.test_client()

    def tearDown(self):
        pass

    def test_rootUrl(self):
        response = self.app.get("/", follow_redirects=True)
        assert 200 == response.status_code
        assert b"Hello World!" in response.data

    def test_authorization(self):
        # Injects new auth keys
        flaskapp.yb.change_authorized_keys(["auth_for_tests_1", "auth_for_tests_2"])

        data = {
            "intent": "test_intent",
            "params": {"test_param_1": "test_value_1"}
        }
        response = self.app.post(
            "{}/intent".format(flaskapp.BASIC_ADDRESS),
            headers={"X-Authorization": "test_key_1"},
            data=json.dumps(data), # Has to be inside dumps
            content_type="application/json", # Has to be specified
            follow_redirects=True
        )
        assert 401 == response.status_code

        response = self.app.post(
            "{}/intent".format(flaskapp.BASIC_ADDRESS),
            headers={"X-Authorization": "auth_for_tests_1"},
            data=json.dumps(data), # Has to be inside dumps
            content_type="application/json", # Has to be specified
            follow_redirects=True
        )
        assert 200 == response.status_code

        response = self.app.post(
            "{}/intent".format(flaskapp.BASIC_ADDRESS),
            headers={"X-Authorization": "auth_for_tests_2"},
            data=json.dumps(data), # Has to be inside dumps
            content_type="application/json", # Has to be specified
            follow_redirects=True
        )
        assert 200 == response.status_code

    def test_badRequest(self):
        # Injects new auth keys
        flaskapp.yb.change_authorized_keys(["auth_for_tests_1"])

        # no json at all
        response = self.app.post(
            "{}/intent".format(flaskapp.BASIC_ADDRESS),
            headers={"X-Authorization": "auth_for_tests_1"},
            follow_redirects=True
        )
        assert 400 == response.status_code

        # Missing json, but content_type specified
        response = self.app.post(
            "{}/intent".format(flaskapp.BASIC_ADDRESS),
            headers={"X-Authorization": "auth_for_tests_1"},
            content_type="application/json",
            follow_redirects=True
        )
        assert 400 == response.status_code

        # Wrong intent name
        data = {
            "intent_ZZZ": "test_intent",
        }
        response = self.app.post(
            "{}/intent".format(flaskapp.BASIC_ADDRESS),
            headers={"X-Authorization": "auth_for_tests_1"},
            data=json.dumps(data),
            content_type="application/json",
            follow_redirects=True
        )
        assert 400 == response.status_code

        # Only intent, but good because parameters are not required
        data = {
            "intent": "test_intent",
        }
        response = self.app.post(
            "{}/intent".format(flaskapp.BASIC_ADDRESS),
            headers={"X-Authorization": "auth_for_tests_1"},
            data=json.dumps(data),
            content_type="application/json",
            follow_redirects=True
        )
        assert 200 == response.status_code

        # Good intent, but lack of mandatory parameters
        data = {
            "intent": GlobalBag.ECHO_MESSAGE_INTENT,
        }
        response = self.app.post(
            "{}/intent".format(flaskapp.BASIC_ADDRESS),
            headers={"X-Authorization": "auth_for_tests_1"},
            data=json.dumps(data),
            content_type="application/json",
            follow_redirects=True
        )
        assert 400 == response.status_code

        # Good intent, but wrong parameters
        data = {
            "intent": GlobalBag.ECHO_MESSAGE_INTENT,
            "params": {"zzzz": "Good morning"}
        }
        response = self.app.post(
            "{}/intent".format(flaskapp.BASIC_ADDRESS),
            headers={"X-Authorization": "auth_for_tests_1"},
            data=json.dumps(data),
            content_type="application/json",
            follow_redirects=True
        )
        assert 400 == response.status_code

        # Good intent and good parameters
        data = {
            "intent": GlobalBag.ECHO_MESSAGE_INTENT,
            "params": {GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE: "Good morning"}
        }
        response = self.app.post(
            "{}/intent".format(flaskapp.BASIC_ADDRESS),
            headers={"X-Authorization": "auth_for_tests_1"},
            data=json.dumps(data),
            content_type="application/json",
            follow_redirects=True
        )
        assert 200 == response.status_code
