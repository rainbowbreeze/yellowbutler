"""
From sentences in natural language, derive intents and arguments
"""
from yellowbot.globalbag import GlobalBag


class NluEngine:
    """
    Very simply implementation of an NLU engine based on simple regex rules:
    transform sentences in intent and parameters
    """
    def __init__(self):
        pass

    def infer_intent_and_args(self, message):
        """
        Given a sentence, infers intent and arguments

        :param message: the sentence to understand
        :type message: str

        :return: intent as string and arguments as a collection of values
        :rtype: str, dict
        """
        # Initial checks
        if message is None: return None, None

        intent = None
        params = {}  # A dict, not a set (unordered collection of unique items, use set() to initialize)

        # Check for EasyNido intent
        headers = ["asilo", "/asilo"]
        if any(message.lower().startswith(header) for header in headers):
            intent = GlobalBag.EASYNIDO_INTENT_REPORT
            return intent, params

        # Checks for Music Trace intent
        # SoundHound word is the word trigger
        if message.lower().find("soundhound") > 0:
            # Finds the author and title, with Italian or English message
            if message.lower().startswith("appena usato"):
                # Italian language
                begin_search_string = "Appena usato SoundHound per trovare "
                separator_string = " di "
            elif message.lower().startswith("just used"):
                # English language
                begin_search_string = "Just used SoundHound to find "
                separator_string = " by "
            else:
                # Unknown language
                begin_search_string = None

            if begin_search_string:
                end_pos = message.find("https://")
                title_and_author = message[len(begin_search_string):end_pos-1].strip()
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

        # Checks for other intents

        return intent, params
