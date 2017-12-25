"""
Test for the NLU engine
"""

from yellowbot.globalbag import GlobalBag
from yellowbot.nluengine import NluEngine


class TestNluEngine(object):

    def test_rules(self):
        nlu_engine = NluEngine()

        # Try some sentences
        intent, params = nlu_engine.infer_intent_and_args("Test message")
        assert intent is None
        assert params == {}

        intent, params = nlu_engine.infer_intent_and_args("Echo very long message")
        assert intent == GlobalBag.ECHO_MESSAGE_INTENT
        assert GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE in params
        assert params.get(GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE) == "very long message"
        intent, params = nlu_engine.infer_intent_and_args("Say whatever you want!")
        assert intent == GlobalBag.ECHO_MESSAGE_INTENT
        assert GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE in params
        assert params.get(GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE) == "whatever you want!"
        intent, params = nlu_engine.infer_intent_and_args("Repeat a sentence of your choice")
        assert intent == GlobalBag.ECHO_MESSAGE_INTENT
        assert GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE in params
        assert params.get(GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE) == "a sentence of your choice"
