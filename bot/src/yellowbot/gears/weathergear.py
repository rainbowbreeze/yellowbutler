"""A YellowBot gear to get weather forecast

Info at https://github.com/AnthonyBloomer/weather-api

Requirements
-requests
"""

from typing import Any, ClassVar, Dict, List, Optional, Union
import requests
import arrow

from yellowbot.gears.basegear import BaseGear
from yellowbot.globalbag import GlobalBag
from yellowbot.loggingservice import LoggingService


class WeatherGear(BaseGear):
    """Get the weather condition from DarkSky Weather service
    """

    INTENTS: ClassVar[List[str]]= [GlobalBag.WEATHER_FORECAST_INTENT]
    PARAM_LOCATION: ClassVar[str] = GlobalBag.WEATHER_FORECAST_PARAM_LOCATION  # The latitude and longitude of the city
    PARAM_CITY_NAME: ClassVar[str] = GlobalBag.WEATHER_FORECAST_PARAM_CITY_NAME  # The city name

    def __init__(
        self,
        api_key: str
    ) -> None:
        super().__init__(self.__class__.__name__, self.INTENTS)
        self._logger = LoggingService.get_logger(__name__)
        self._api_key = api_key

    def process_intent(
        self,
        intent: str,
        params: Dict[str, Any]
    ) -> Optional[str]:
        return self._read_weather_from_darksky(intent, params)

    def _read_weather_from_darksky(
        self,
        intent: str,
        params: Dict[str, Any]
    ) -> Optional[str]:
        """Read weather information from DarkSky APIs
        :param intent:
        :param params:
        :return:
        """

        if WeatherGear.INTENTS[0] != intent:
            message = "Call to {} using wrong intent {}".format(__name__, intent)
            self._logger.info(message)
            return message
        if WeatherGear.PARAM_CITY_NAME not in params:
            return "Missing {} parameter in the request_".format(WeatherGear.PARAM_CITY_NAME)
        city_name = params[WeatherGear.PARAM_CITY_NAME]
        if WeatherGear.PARAM_LOCATION not in params:
            # Adds some defaults latitude and longitude data
            if "pavia" == city_name.lower():
                latlng = "45.19205,9.15917"
            elif "milano" == city_name.lower():
                latlng = "45.4642,9.1900"
            elif "fabriano" == city_name.lower():
                latlng = "43.3450,12.9062"
            elif "civitanova" == city_name.lower():
                latlng = "43.3048,13.7218"
            else:
                return "Missing {} parameter in the request".format(WeatherGear.PARAM_LOCATION)
        else:
            latlng = params[WeatherGear.PARAM_LOCATION]

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
            current_temperature = round(results["currently"]["temperature"])
            week_summary = results["daily"]["summary"]
            daily_data = results["daily"]["data"][0]
            daily_summary = daily_data["summary"]
            daily_temperature_max = round(daily_data["temperatureMax"])
            daily_temperature_min = round(daily_data["temperatureMin"])
            daily_sunrise_epoch = daily_data["sunriseTime"]
            daily_sunrise_time = self._from_epoch_to_time(daily_sunrise_epoch, timezone)
            daily_sunset_epoch = daily_data["sunsetTime"]
            daily_sunset_time = self._from_epoch_to_time(daily_sunset_epoch, timezone)
            return "A {} attualmente {} e {}°C.\n" \
                   "Oggi {}, con temperatura min {}°C e max {}°C. Alba alle {} e tramonto alle {}.\n" \
                   "Nei prossimi giorni {}".format(
                city_name,
                current_summary,
                current_temperature,
                daily_summary,
                daily_temperature_min,
                daily_temperature_max,
                daily_sunrise_time,
                daily_sunset_time,
                week_summary
            )
        except BaseException as e:
            self._logger.exception(e)
            return "Exception happened while parsing weather data {}".format(repr(e))

    def _from_epoch_to_time(
        self,
        epoch: Union[str, int],
        timezone: str
    ) -> str:
        """Transform an Epoch time to a time

        :param epoch: Epoch time
        :type epoch: str or int

        :param timezone: timezone
        :type timezone: str

        :return: the time converted
        :rtype: str
        """

        time = arrow.get(epoch)  # UTC
        time = time.to(timezone)  # Local time
        return str(time.format("HH:mm"))
