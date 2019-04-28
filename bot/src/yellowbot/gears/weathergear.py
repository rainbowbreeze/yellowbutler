"""
A YellowBot gear to get weather forecast

Info at https://github.com/AnthonyBloomer/weather-api

Requirements
-requests
"""
import requests
import arrow

from yellowbot.gears.basegear import BaseGear
from yellowbot.globalbag import GlobalBag
from yellowbot.loggingservice import LoggingService


class WeatherGear(BaseGear):
    """
    Get the weather condition from Yahoo! Weather service
    """
    INTENTS = [GlobalBag.WEATHER_FORECAST_INTENT]
    PARAM_LOCATION = GlobalBag.WEATHER_FORECAST_PARAM_LOCATION  # The latitude and longitude of the city
    PARAM_CITY_NAME = GlobalBag.WEATHER_FORECAST_PARAM_CITY_NAME  # The city name

    def __init__(self, api_key):
        BaseGear.__init__(self, WeatherGear.__name__, self.INTENTS)
        self._logger = LoggingService.get_logger(__name__)
        self._api_key = api_key

    def process_intent(self, intent, params):
        return self._read_weather_from_darksky(intent, params)

    def _read_weather_from_darksky(self, intent, params):
        """
        Read weather information from DarkSky APIs
        :param intent:
        :param params:
        :return:
        """

        if WeatherGear.INTENTS[0] != intent:
            message = "Call to {} using wrong intent {}".format(__name__, intent)
            self._logger.info(message)
            return message
        if WeatherGear.PARAM_LOCATION not in params:
            return "Missing {} parameter in the request".format(WeatherGear.PARAM_LOCATION)
        if WeatherGear.PARAM_CITY_NAME not in params:
            return "Missing {} parameter in the request".format(WeatherGear.PARAM_CITY_NAME)

        latlng = params[WeatherGear.PARAM_LOCATION]
        city_name = params[WeatherGear.PARAM_CITY_NAME]
        self._logger.info("Searching weather condition for city {} at location {}".format(city_name, latlng))

        url = "https://api.darksky.net/forecast/{}/{}?{}".format(
            self._api_key,
            latlng,
            "exclude=minutely,hourly,alerts,flags&units=si&lang=it"
        )
        try:
            req = requests.get(url)
            if not req.ok:
                req.raise_for_status()
            results = req.json()
        except BaseException as e:
            self._logger.exception(e)
            return "Error while getting weather information {}".format(repr(e))

        try:
            timezone = results["timezone"]
            current_summary = results["currently"]["summary"]
            current_temperature = results["currently"]["temperature"]
            week_summary = results["daily"]["summary"]
            daily_data = results["daily"]["data"][0]
            daily_summary = daily_data["summary"]
            daily_temperature_max = daily_data["temperatureMax"]
            daily_temperature_min = daily_data["temperatureMin"]
            daily_sunrise_epoch = daily_data["sunriseTime"]
            daily_sunrise_time = self._from_epoch_to_time(daily_sunrise_epoch, timezone)
            daily_sunset_epoch = daily_data["sunsetTime"]
            daily_sunset_time = self._from_epoch_to_time(daily_sunset_epoch, timezone)
            return "A {} attualmente {} e {}°C.\n" \
                   "Per i prossimi giorni si prevede {}.\n" \
                   "Oggi {}, con min {}°, max {}°, alba {} tramonto {}".format(
                city_name,
                current_summary,
                current_temperature,
                week_summary,
                daily_summary,
                daily_temperature_min,
                daily_temperature_max,
                daily_sunrise_time,
                daily_sunset_time
            )
        except BaseException as e:
            self._logger.exception(e)
            return "Exception happened while parsing weather data {}".format(repr(e))

    def _from_epoch_to_time(self, epoch, timezone):
        """
        Transform an Epoch time to a time

        :param epoch: Epoch time
        :type epoch: str or int

        :param timezone: timezone
        :type timezone: str

        :return: the time converted
        :rtype: str
        """

        time = arrow.get(epoch)  # UTC
        time = time.to(timezone)  # Local time
        return time.format("HH:mm")
