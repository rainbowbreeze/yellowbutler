"""
From sentences in natural language, derive intents and parameters
"""
from typing import Dict, Optional, Tuple, Union
from yellowbot.globalbag import GlobalBag


class NluEngine:
    """Very simply implementation of an NLU engine based on simple regex rules:
    transform sentences in intent and parameters
    """

    def __init__(self) -> None:
        pass

    def infer_intent_and_args(
        self,
        message: Optional[str]
    ) -> Tuple[Optional[str], Dict[str, Union[str, bool]]]:
        """Given a sentence, infers intent and arguments

        :param message: the sentence to understand
        :type message: str

        :return: intent as string and arguments as a collection of values
        :rtype: str, dict
        """
        # Initial checks
        if message is None: return None, {}

        intent = None
        params: Dict[str, Union[str, bool]] = {}  # A dict, not a set (unordered collection of unique items, use set() to initialize)

        # Check for EasyNido intent
        headers = ["asilo", "/asilo"]
        if any(message.lower().startswith(header) for header in headers):
            intent = GlobalBag.EASYNIDO_INTENT_REPORT
            return intent, params

        # Check for weather intent
        headers = ["weather", "meteo", "tempo"]
        for header in headers:
            if message.lower().startswith(header):
                intent = GlobalBag.WEATHER_FORECAST_INTENT
                location_name = message[len(header):].strip()
                params[GlobalBag.WEATHER_FORECAST_PARAM_CITY_NAME] = location_name
                return intent, params

        # Checks for Music Trace intent
        # SoundHound word is the word trigger
        if message.lower().find("soundhound") > 0:
            # Finds the author and title, with Italian or English message
            begin_search_string = None
            end_string = None
            separator_string = None
            if message.lower().startswith("appena usato"):
                # Italian language
                begin_search_string = "Appena usato SoundHound per trovare "
                separator_string = " di "
                end_string = "https://"
            elif message.lower().startswith("ho trovato "):
                begin_search_string = "Ho trovato "
                separator_string = " di "
                end_string = " con SoundHound, credo che ti piacer"
            elif message.lower().startswith("just used "):
                # English language
                begin_search_string = "Just used SoundHound to find "
                separator_string = " by "
                end_string = "https://"
            elif message.lower().startswith("i found "):
                # English language
                begin_search_string = "I found "
                separator_string = " by "
                end_string = "https://"
            else:
                # Unknown language
                begin_search_string = None

            if begin_search_string and end_string and separator_string:
                end_pos = message.find(end_string)
                title_and_author = message[len(begin_search_string):end_pos].strip()
                end_pos = title_and_author.find(separator_string)
                title = title_and_author[:end_pos].strip()
                author = title_and_author[end_pos + len(separator_string):].strip()
                intent = GlobalBag.TRACE_MUSIC_INTENT
                params[GlobalBag.TRACE_MUSIC_PARAM_TITLE] = title
                params[GlobalBag.TRACE_MUSIC_PARAM_AUTHOR] = author
                return intent, params

        # Checks for echo intent
        headers = ["echo", "repeat", "say"]
        # if any(message.lower().startswith(header) for header in headers):  # skip standard headers
        for header in headers:
            if message.lower().startswith(header):
                intent = GlobalBag.ECHO_MESSAGE_INTENT
                params[GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE] = message[len(header):].strip()
                return intent, params

        # Checks for CommitStrip intent
        headers = ["commitstrip", "/commitstrip"]
        if any(message.lower().startswith(header) for header in headers):
            intent = GlobalBag.COMMITSTRIP_INTENT
            return intent, params

        # Checks for CheckForNews intent
        headers = ["checkfornews", "/checkfornews"]
        if any(message.lower().startswith(header) for header in headers):
            intent = GlobalBag.CHECKFORNEWS_INTENT
            params[GlobalBag.CHECKFORNEWS_PARAM_SILENT] = False
            return intent, params

        # Checks for other intents

        return intent, params
