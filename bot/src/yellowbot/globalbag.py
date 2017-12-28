"""
Global constrains for YellowBot

For reference: http://radek.io/2011/07/21/static-variables-and-methods-in-python/
"""


class GlobalBag:
    """
    Bag for global static vars
    """

    # Echo message gear
    ECHO_MESSAGE_INTENT = "echo_message"
    ECHO_MESSAGE_PARAM_MESSAGE = "message"

    # Trace music gear
    TRACE_MUSIC_INTENT = "trace_music"
    TRACE_MUSIC_PARAM_TITLE = "title"
    TRACE_MUSIC_PARAM_AUTHOR = "author"

    # Kindergarten gear
    KINDERGARTEN_INTENT_CHECK = "kindergarten_check"
    KINDERGARTEN_INTENT_REPORT = "kindergarten_report"

    # Interaction surfaces
    SURFACE_TELEGRAM_BOT_LURCH = "Telegram-Lurch"  # Lurch telegram bot


