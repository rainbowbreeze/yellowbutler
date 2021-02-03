"""
Global constrains for YellowBot

For reference: http://radek.io/2011/07/21/static-variables-and-methods-in-python/
"""


class GlobalBag:
    """
    Bag for global static vars
    """

    # EasyNido gear
    EASYNIDO_INTENT_REPORT = "easynido_report"

    # Echo message gear
    ECHO_MESSAGE_INTENT = "echo_message"
    ECHO_MESSAGE_PARAM_MESSAGE = "message"

    # Trace music gear
    TRACE_MUSIC_INTENT = "trace_music"
    TRACE_MUSIC_PARAM_TITLE = "title"
    TRACE_MUSIC_PARAM_AUTHOR = "author"

    # Weather forecast
    WEATHER_FORECAST_INTENT = "weather_forecast"
    WEATHER_FORECAST_PARAM_LOCATION = "latlng"
    WEATHER_FORECAST_PARAM_CITY_NAME = "city_name"

    # Send a message
    SEND_MESSAGE_INTENT = "send_message"
    SEND_MESSAGE_PARAM_SURFACE_ID = "surface_id"
    SEND_MESSAGE_PARAM_CHANNEL_ID = "chat_id"
    SEND_MESSAGE_PARAM_TEXT = "text"

    # Notify Admins
    NOTIFY_ADMIN_INTENT = "notify_admin"
    NOTIFY_ADMIN_PARAM_MESSAGE = "message"

    # CommitStrip 
    COMMITSTRIP_INTENT = "commitstrip"
    COMMITSTRIP_PARAM_SILENT = "silent"

    # NewsReporter
    CHECKFORNEWS_INTENT = "checkfornews"
    
    # Interaction surfaces
    SURFACE_TELEGRAM_BOT_LURCH = "Telegram-Lurch"  # Lurch telegram bot
    SURFACE_NOTIFY_ADMIN = "NotifyAdmin"  # Notification channel for admin

    # Database file name
    DATABASE_FILE = "yellowbot_db.json"
    # File with the configurations
    CONFIG_FILE = "yellowbot_config.json"
    # File with the tasks for the scheduler service
    SCHEDULER_FILE = "yellowbot_tasks.json"

    # Quick and dirty way to setup a proper test environment
    TEST_ENVIRONMENT = False

