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
        self.assertIsNone(intent)
        self.assertEqual(0, len(params))

    def test_echo_message_rules(self):
        intent, params = self.nlu_engine.infer_intent_and_args("Echo very long message")
        self.assertEqual(GlobalBag.ECHO_MESSAGE_INTENT, intent)
        assert GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE in params
        assert params.get(GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE) == "very long message"
        intent, params = self.nlu_engine.infer_intent_and_args("Say whatever you want!")
        self.assertEqual(GlobalBag.ECHO_MESSAGE_INTENT, intent)
        assert GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE in params
        assert params.get(GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE) == "whatever you want!"
        intent, params = self.nlu_engine.infer_intent_and_args("Repeat a sentence of your choice")
        self.assertEqual(GlobalBag.ECHO_MESSAGE_INTENT, intent)
        assert GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE in params
        assert params.get(GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE) == "a sentence of your choice"

    def test_music_rules(self):
        sentence = "Appena usato SoundHound per trovare You Could Be Mine di Guns N' Roses https://bnc.lt/Scoe/jrtmcTrzMH"
        intent, params = self.nlu_engine.infer_intent_and_args(sentence)
        self.assertEqual(GlobalBag.TRACE_MUSIC_INTENT, intent)
        assert GlobalBag.TRACE_MUSIC_PARAM_AUTHOR in params
        assert params.get(GlobalBag.TRACE_MUSIC_PARAM_AUTHOR) == "Guns N' Roses"
        assert GlobalBag.TRACE_MUSIC_PARAM_TITLE in params
        assert params.get(GlobalBag.TRACE_MUSIC_PARAM_TITLE) == "You Could Be Mine"

        sentence = "Just used SoundHound to find Who Do You Love? by George Thorogood https://bnc.lt/Scoe/PKD7kWbXRG"
        intent, params = self.nlu_engine.infer_intent_and_args(sentence)
        self.assertEqual(GlobalBag.TRACE_MUSIC_INTENT, intent)
        assert GlobalBag.TRACE_MUSIC_PARAM_AUTHOR in params
        assert params.get(GlobalBag.TRACE_MUSIC_PARAM_AUTHOR) == "George Thorogood"
        assert GlobalBag.TRACE_MUSIC_PARAM_TITLE in params
        assert params.get(GlobalBag.TRACE_MUSIC_PARAM_TITLE) == "Who Do You Love?"


        sentence = "Ho trovato Highway Tune di Greta Van Fleet con SoundHound, credo che ti piacerà! https://bnc.lt/Scoe/q7QjpeW5zD"
        intent, params = self.nlu_engine.infer_intent_and_args(sentence)
        self.assertEqual(GlobalBag.TRACE_MUSIC_INTENT, intent)
        self.assertEqual(2, len(params))
        self.assertEqual("Greta Van Fleet", params.get(GlobalBag.TRACE_MUSIC_PARAM_AUTHOR))
        self.assertEqual("Highway Tune", params.get(GlobalBag.TRACE_MUSIC_PARAM_TITLE))

    def test_weather_rules(self):
        sentence = "Weather Pavia"
        intent, params = self.nlu_engine.infer_intent_and_args(sentence)
        self.assertEqual(GlobalBag.WEATHER_FORECAST_INTENT, intent)
        self.assertEqual(1, len(params))
        self.assertEqual("Pavia", params.get(GlobalBag.WEATHER_FORECAST_PARAM_CITY_NAME))

        sentence = "Meteo Milano, Italy"
        intent, params = self.nlu_engine.infer_intent_and_args(sentence)
        self.assertEqual(GlobalBag.WEATHER_FORECAST_INTENT, intent)
        self.assertEqual(1, len(params))
        self.assertEqual("Milano, Italy", params.get(GlobalBag.WEATHER_FORECAST_PARAM_CITY_NAME))

    def test_checkfornews_rules(self):
        sentence = "/checkfornews"
        intent, params = self.nlu_engine.infer_intent_and_args(sentence)
        self.assertEqual(GlobalBag.CHECKFORNEWS_INTENT, intent)
        self.assertEqual(1, len(params))
        self.assertFalse(params.get(GlobalBag.CHECKFORNEWS_PARAM_SILENT))

        sentence = "/newssources"
        intent, params = self.nlu_engine.infer_intent_and_args(sentence)
        self.assertEqual(GlobalBag.NEWSSOURCES_INTENT, intent)
        self.assertEqual(0, len(params))
