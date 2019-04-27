"""
Read configurations from a file
"""
import json
import os

from json_minify import json_minify

from yellowbot.globalbag import GlobalBag
from yellowbot.loggingservice import LoggingService


class ConfigService:
    def __init__(self,
                 config_file=GlobalBag.CONFIG_FILE):
        """

        :param config_file: config file with several values. By default, the
        file yellowbot_config.json in the same folder of this file is used,
        but feel free to point to any other file. If only the file name is
        used, the assumption it is in the same folder of this file
        :type config_file: str
        """
        # Create the logger and initialise it
        self._logger = LoggingService.get_logger(__name__)
        self._logger.info("Config service is starting")

        # Load the config file
        self._load_config_file(config_file)

    def _load_config_file(self, config_file):
        """
        Load config key/value pairs from a file
        :param config_file: name of the file. Can be full path or, otherwise,
        same folder of this class is considered
        :type config_file: str

        :return:
        """
        self._config = {}
        if not os.path.isfile(config_file):
            # Folder where this file is, can work also without the abspath,
            #  but better for debug so full path is traced in the error
            base_folder = os.path.abspath(os.path.dirname(__file__))
            full_config_path = os.path.join(base_folder, config_file)  # combine with the config file name
        else:
            full_config_path = config_file
        # Now if has the file and full path with configurations
        if os.path.isfile(full_config_path):
            with open(full_config_path, 'r') as f:
                json_with_comment = open(full_config_path).read()
                self._config = json.loads(json_minify(json_with_comment))
        else:
            raise ValueError("Cannot find configuration file {}".format(full_config_path))
        # Checks if the config files has real values
        if len(self._config.keys()) == 0:
            raise ValueError("Empty configuration file {}".format(full_config_path))

    def get_config(self, key_to_read, throw_error=True):
        """
        Read a value from the configuration, throwing an error if it doesn't exist
        :param key_to_read: the key to read
        :type key_to_read: str

        :param throw_error: if False, doesn't throw an error, but return None instead
        :type throw_error: bool

        :return: the object associated wit the config key
        """
        try:
            return self._config[key_to_read]
        except KeyError as e:
            if throw_error:
                raise ValueError(
                    "Non existing {} value in the config, please add it".format(key_to_read))
            else:
                return None

    def change_authorized_keys(self, new_keys):
        """
        Substitutes old authorization keys with new ones. Useful for testing
        purposes
        :param new_keys: new keys to use
        :type new_keys: str
        """
        self._config["authorized_keys"] = new_keys
