"""
A YellowBot gear to get weather forecast

Info at https://github.com/AnthonyBloomer/weather-api

Requirements
- weather-api
"""
from weather import Weather

from yellowbot.gears.basegear import BaseGear
from yellowbot.globalbag import GlobalBag
from yellowbot.loggingservice import LoggingService


class WeatherGear(BaseGear):
    """
    Remember different kind of music
    """
    INTENTS = [GlobalBag.WEATHER_FORECAST_INTENT]
    PARAM_LOCATION = GlobalBag.WEATHER_FORECAST_PARAM_LOCATION  # The message to echo

    def __init__(self):
        BaseGear.__init__(self, WeatherGear.__name__, self.INTENTS)
        self._weather = Weather()
        self._logger = LoggingService.get_logger(__name__)

    def _check_parameters(self, params):
        return WeatherGear.PARAM_LOCATION in params

    def process_intent(self, intent, params):
        location_name = params[WeatherGear.PARAM_LOCATION]
        self._logger.info("Searching weather condition for %s", location_name)

        location_woeid = self._weather.lookup_by_location(location_name)
        if location_woeid:
            condition = location_woeid.condition()
            return "Weather forecast for {} in {}: {}, temp {}".format(
                condition.date(),
                location_name,
                condition.text(),
                condition.temp()
            )
        else:
            self._logger.info("Cannot find a woeid code for the given location")
            return "Sorry, I don't know how to provide weather forecast for {}".format(
                location_name
            )
