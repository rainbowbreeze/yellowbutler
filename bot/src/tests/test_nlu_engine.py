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
