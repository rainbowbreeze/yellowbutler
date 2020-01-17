"""
Test for the NLU engine
"""
from unittest import TestCase

from yellowbot.globalbag import GlobalBag
from yellowbot.nluengine import NluEngine


class TestNluEngine(TestCase):
    def setUp(self):
        self.nlu_engine = NluEngine()

    def tearDown(self):
        pass

    def test_empty_sentence(self):
        intent, params = self.nlu_engine.infer_intent_and_args("Test message")
        assert intent is None
        assert params == {}

    def test_echo_message_rules(self):
        intent, params = self.nlu_engine.infer_intent_and_args("Echo very long message")
        assert intent == GlobalBag.ECHO_MESSAGE_INTENT
        assert GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE in params
        assert params.get(GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE) == "very long message"
        intent, params = self.nlu_engine.infer_intent_and_args("Say whatever you want!")
        assert intent == GlobalBag.ECHO_MESSAGE_INTENT
        assert GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE in params
        assert params.get(GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE) == "whatever you want!"
        intent, params = self.nlu_engine.infer_intent_and_args("Repeat a sentence of your choice")
        assert intent == GlobalBag.ECHO_MESSAGE_INTENT
        assert GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE in params
        assert params.get(GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE) == "a sentence of your choice"

    def test_music_rules(self):
        sentence = "Appena usato SoundHound per trovare You Could Be Mine di Guns N' Roses https://bnc.lt/Scoe/jrtmcTrzMH"
        intent, params = self.nlu_engine.infer_intent_and_args(sentence)
        assert intent == GlobalBag.TRACE_MUSIC_INTENT
        assert GlobalBag.TRACE_MUSIC_PARAM_AUTHOR in params
        assert params.get(GlobalBag.TRACE_MUSIC_PARAM_AUTHOR) == "Guns N' Roses"
        assert GlobalBag.TRACE_MUSIC_PARAM_TITLE in params
        assert params.get(GlobalBag.TRACE_MUSIC_PARAM_TITLE) == "You Could Be Mine"

        sentence = "Just used SoundHound to find Who Do You Love? by George Thorogood https://bnc.lt/Scoe/PKD7kWbXRG"
        intent, params = self.nlu_engine.infer_intent_and_args(sentence)
        assert intent == GlobalBag.TRACE_MUSIC_INTENT
        assert GlobalBag.TRACE_MUSIC_PARAM_AUTHOR in params
        assert params.get(GlobalBag.TRACE_MUSIC_PARAM_AUTHOR) == "George Thorogood"
        assert GlobalBag.TRACE_MUSIC_PARAM_TITLE in params
        assert params.get(GlobalBag.TRACE_MUSIC_PARAM_TITLE) == "Who Do You Love?"


        sentence = "Ho trovato Highway Tune di Greta Van Fleet con SoundHound, credo che ti piacerà! https://bnc.lt/Scoe/q7QjpeW5zD"
        intent, params = self.nlu_engine.infer_intent_and_args(sentence)
        assert intent == GlobalBag.TRACE_MUSIC_INTENT
        assert GlobalBag.TRACE_MUSIC_PARAM_AUTHOR in params
        assert params.get(GlobalBag.TRACE_MUSIC_PARAM_AUTHOR) == "Greta Van Fleet"
        assert GlobalBag.TRACE_MUSIC_PARAM_TITLE in params
        assert params.get(GlobalBag.TRACE_MUSIC_PARAM_TITLE) == "Highway Tune"

    def test_weather_rules(self):
        sentence = "Weather Pavia"
        intent, params = self.nlu_engine.infer_intent_and_args(sentence)
        assert intent == GlobalBag.WEATHER_FORECAST_INTENT
        assert GlobalBag.WEATHER_FORECAST_PARAM_CITY_NAME in params
        assert params.get(GlobalBag.WEATHER_FORECAST_PARAM_CITY_NAME) == "Pavia"

        sentence = "Meteo Milano, Italy"
        intent, params = self.nlu_engine.infer_intent_and_args(sentence)
        assert intent == GlobalBag.WEATHER_FORECAST_INTENT
        assert GlobalBag.WEATHER_FORECAST_PARAM_CITY_NAME in params
        assert params.get(GlobalBag.WEATHER_FORECAST_PARAM_CITY_NAME) == "Milano, Italy"
