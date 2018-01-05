"""
A YellowBot gear to get weather forecast

Info at https://github.com/AnthonyBloomer/weather-api

Requirements
-requests
"""
import requests

from yellowbot.gears.basegear import BaseGear
from yellowbot.globalbag import GlobalBag
from yellowbot.loggingservice import LoggingService


class WeatherGear(BaseGear):
    """
    Get the weather condition from Yahoo! Weather service
    """
    INTENTS = [GlobalBag.WEATHER_FORECAST_INTENT]
    PARAM_LOCATION = GlobalBag.WEATHER_FORECAST_PARAM_LOCATION  # The message to echo

    _URL = 'http://query.yahooapis.com/v1/public/yql'

    def __init__(self):
        BaseGear.__init__(self, WeatherGear.__name__, self.INTENTS)
        self._logger = LoggingService.get_logger(__name__)

    def _check_parameters(self, params):
        return WeatherGear.PARAM_LOCATION in params

    def process_intent(self, intent, params):
        """
        How Yahoo weather works

        Basic Python code to query the API
        https://developer.yahoo.com/weather/#python

        select item.condition from weather.forecast where woeid = 2487889
        https://query.yahooapis.com/v1/public/yql?q=select%20item.condition%20from%20weather.forecast%20where%20woeid%20%3D%202487889&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys

        select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="Rome, Italy") and 'u=c'

        :param intent:
        :param params:
        :return:
        """
        location_name = params[WeatherGear.PARAM_LOCATION]
        self._logger.info("Searching weather condition for %s", location_name)

        # Test different options using
        #  https://developer.yahoo.com/weather/
        # Using Celsius instead of Fahrenheit
        #  https://stackoverflow.com/questions/21092164/return-yahoo-weather-api-data-in-celsius-using-yql
        url = "{}?q=select item, astronomy from weather.forecast " \
              "where woeid in (select woeid from geo.places(1) where text='{}') and u='c'" \
              "&format=json"\
            .format(self._URL, location_name)

        try:
            req = requests.get(url)
            if not req.ok:
                req.raise_for_status()
            results = req.json()
        except BaseException as e:
            self._logger.exception(e)
            return "Error while getting weather information {}".format(repr(e))

        try:
            if int(results['query']['count']) > 0:
                wo = results['query']['results']['channel']
                astronomy = wo['astronomy']
                today_forecast = wo['item']['forecast'][0]
                return "Today's weather for {}: {}, min {}, max {}. Sunrise {}, sunset {}".format(
                    location_name,
                    today_forecast['text'],
                    today_forecast['low'],
                    today_forecast['high'],
                    astronomy['sunrise'],
                    astronomy['sunset']
                )
            else:
                self._logger.info("No weather data for location %s\n Result is %s",
                                     location_name,
                                     results)
                return "Sorry, I don't know how to provide weather forecast for {}".format(
                    location_name)
        except BaseException as e:
            self._logger.exception(e)
            return "Exception happened while parsing weather data {}".format(repr(e))

