"""
Gear to analyse results from Easynido
"""
from yellowbot.gears.basegear import BaseGear
from yellowbot.globalbag import GlobalBag


class EasyNidoGear(BaseGear):
    """
    Checks for EasyNido data
    """
    INTENTS = [GlobalBag.EASYNIDO_INTENT]

    def __init__(self, datastore_service):
        """

        :param datastore_service: service to manage persistent storage of data
        """
        BaseGear.__init__(self, EasyNidoGear.__name__, self.INTENTS)
        self._datastore = datastore_service

    def _check_parameters(self, params):
        return True

    def process_intent(self, intent, params):
        pass

    def parse_webservice_data(self, html_to_parse):
        """
        Given the html to parse, retrieve the different activities
        :param html_to_parse:
        :return:
        """
        return None
