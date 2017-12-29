"""
Global constrains for YellowBot

For reference: http://radek.io/2011/07/21/static-variables-and-methods-in-python/
"""


class GlobalBag:
    """
    Bag for global static vars
    """

    # EasyNido gear
    EASYNIDO_INTENT = "easynido"

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

    # Database file name
    DATABASE_FILE = "yellowbot_db.json"

    # Quick and dirty way to setup a proper test environment
    TEST_ENVIRONMENT = False

