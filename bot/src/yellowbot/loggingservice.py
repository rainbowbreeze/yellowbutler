"""Manage logs for the application

More info at: https://docs.python.org/3.7/howto/logging.html

Best way to log an exception, with python 2.x retrocompatibility:
  self._logger.exception("Error process the request %s", err)
Otherwise, use
  self._logger.exception("Error process the request {}".format(err))
This line will report a custom message, the exception error text, and
 a stracktrace

These three produces the same output, as exception method adds Exception info
to the logging message, and the exception error message
  self._logger.exception("Error process the request %s", err)
  self._logger.exception("Error process the request {}".format(err))
  self._logger.exception("Error process the request {}".format(repr(err)), exc_info=err)
"""

import logging


class LoggingService:

    @staticmethod
    def init() -> None:
        logging.basicConfig(
            level=logging.INFO,
            #level=logging.DEBUG,
            format= "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt='%m-%d %H:%M')

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Creates a new logger

        :param name:
        :type name: str, unicode
        :return: return a logger with a specific name, creating it if necessary
        :rtype: Logger
        """
        
        return logging.getLogger(name)
