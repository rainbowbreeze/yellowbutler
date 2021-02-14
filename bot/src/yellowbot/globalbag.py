"""
Global constrains for YellowBot

For reference: http://radek.io/2011/07/21/static-variables-and-methods-in-python/
"""


from typing import ClassVar


class GlobalBag:
    """
    Bag for global static vars
    """

    # EasyNido gear
    EASYNIDO_INTENT_REPORT: ClassVar[str] = "easynido_report"

    # Echo message gear
    ECHO_MESSAGE_INTENT: ClassVar[str] = "echo_message"
    ECHO_MESSAGE_PARAM_MESSAGE: ClassVar[str] = "message"

    # Trace music gear
    TRACE_MUSIC_INTENT: ClassVar[str] = "trace_music"
    TRACE_MUSIC_PARAM_TITLE: ClassVar[str] = "title"
    TRACE_MUSIC_PARAM_AUTHOR: ClassVar[str] = "author"

    # Weather forecast
    WEATHER_FORECAST_INTENT: ClassVar[str] = "weather_forecast"
    WEATHER_FORECAST_PARAM_LOCATION: ClassVar[str] = "latlng"
    WEATHER_FORECAST_PARAM_CITY_NAME: ClassVar[str] = "city_name"

    # Send a message
    SEND_MESSAGE_INTENT: ClassVar[str] = "send_message"
    SEND_MESSAGE_PARAM_SURFACE_ID: ClassVar[str] = "surface_id"
    SEND_MESSAGE_PARAM_CHANNEL_ID: ClassVar[str] = "chat_id"
    SEND_MESSAGE_PARAM_TEXT: ClassVar[str] = "text"

    # Notify Admins
    NOTIFY_ADMIN_INTENT: ClassVar[str] = "notify_admin"
    NOTIFY_ADMIN_PARAM_MESSAGE: ClassVar[str] = "message"

    # NewsReporter
    CHECKFORNEWS_INTENT: ClassVar[str] = "checkfornews"
    CHECKFORNEWS_PARAM_SILENT: ClassVar[str] = "silent"
    
    # Interaction surfaces
    SURFACE_TELEGRAM_BOT_LURCH: ClassVar[str] = "Telegram-Lurch"  # Lurch telegram bot
    SURFACE_NOTIFY_ADMIN: ClassVar[str] = "NotifyAdmin"  # Notification channel for admin

    # Database file name
    DATABASE_FILE: ClassVar[str] = "yellowbot_db.json"
    # File with the configurations
    CONFIG_FILE: ClassVar[str] = "yellowbot_config.json"
    # File with the tasks for the scheduler service
    SCHEDULER_FILE: ClassVar[str] = "yellowbot_tasks.json"

    # Quick and dirty way to setup a proper test environment
    TEST_ENVIRONMENT: ClassVar[bool] = False

