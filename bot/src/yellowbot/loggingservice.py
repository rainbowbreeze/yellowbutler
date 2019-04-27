"""
Manage logs for the application
"""
import logging


class LoggingService:

    @staticmethod
    def init():
        logging.basicConfig(
            level=logging.INFO,
            format= "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt='%m-%d %H:%M')

    @staticmethod
    def get_logger(name):
        """
        Creates a new logger

        :param name:
        :type name: str, unicode
        :return: return a logger with a specific name, creating it if necessary
        :rtype: Logger
        """
        return logging.getLogger(name)
