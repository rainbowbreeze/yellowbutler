"""
Test for the NLU engine
"""

from yellowbot.nluengine import NluEngine


class TestNluEngine(object):

    def test_rules(self):
        nlu_engine = NluEngine()

        # Try some sentences
        intent, params = nlu_engine.infer_intent_and_args("Test message")
        assert intent is None
        assert params is None
