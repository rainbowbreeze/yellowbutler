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

        :param message: the sentence to understand, as a string
        :return: intent as string and arguments as a collection of values
        """
        # Initial checks
        if message is None: return None, None

        intent = None
        params = {}

        # Checks for echo intent
        headers = ["echo", "repeat", "say"]
        # if any(message.lower().startswith(header) for header in headers):  # skip standard headers
        for header in headers:
            if message.lower().startswith(header):
                intent = GlobalBag.ECHO_MESSAGE_INTENT
                params[GlobalBag.ECHO_MESSAGE_PARAM_MESSAGE] = message[len(header):].strip()

        # Checks for Music Trace intent
        # Find SoundHound word
        if message.lower().find("soundhound") > 0:
            # Finds the author and title, with Italian message
            end_pos = message.find("https://")
            title_and_author = message[36:end_pos-1].strip()
            end_pos = title_and_author.find(" di ")
            title = title_and_author[:end_pos].strip()
            author = title_and_author[end_pos+4:].strip()
            intent = GlobalBag.TRACE_MUSIC_INTENT
            params[GlobalBag.TRACE_MUSIC_PARAM_TITLE] = title
            params[GlobalBag.TRACE_MUSIC_PARAM_AUTHOR] = author

        # Checks for other intents

        return intent, params
