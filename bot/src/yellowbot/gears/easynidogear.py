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

    def __init__(self):
        BaseGear.__init__(self, EasyNidoGear.__name__, self.INTENTS)

    def _check_parameters(self, params):
        return True

    def process_intent(self, intent, params):
        pass
