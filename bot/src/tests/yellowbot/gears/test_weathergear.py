"""
Test for weather gear
"""
from unittest import TestCase

from yellowbot.gears.weathergear import WeatherGear
from yellowbot.globalbag import GlobalBag


class TestWeatherGear(TestCase):
    def setUp(self):
        self._gear = WeatherGear("test_darksky_api")
        pass

    def tearDown(self):
        pass

    def test_process_intent(self):
        # Uncomment to check weather condition
        # result = self._gear.process_intent(
        #     GlobalBag.WEATHER_FORECAST_INTENT,
        #     {
        #         GlobalBag.WEATHER_FORECAST_PARAM_LOCATION: "Pavia, Italy"
        #     }
        # )
        # print(result)
        # assert 1==2
        pass
