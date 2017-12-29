"""
Global constrains for YellowBot

For reference: http://radek.io/2011/07/21/static-variables-and-methods-in-python/
"""


class GlobalBag:
    """
    Bag for global static vars
    """

    # EasyNido gear
    EASYNIDO_INTENT_CHECK = "easynido_check"
    EASYNIDO_INTENT_REPORT = "easynido_report"

    # Echo message gear
    ECHO_MESSAGE_INTENT = "echo_message"
    ECHO_MESSAGE_PARAM_MESSAGE = "message"

    # Trace music gear
    TRACE_MUSIC_INTENT = "trace_music"
    TRACE_MUSIC_PARAM_TITLE = "title"
    TRACE_MUSIC_PARAM_AUTHOR = "author"

    # Interaction surfaces
    SURFACE_TELEGRAM_BOT_LURCH = "Telegram-Lurch"  # Lurch telegram bot

    # Database file name
    DATABASE_FILE = "yellowbot_db.json"
    CONFIG_FILE = "yellowbot_config.json"

    # Quick and dirty way to setup a proper test environment
    TEST_ENVIRONMENT = False

