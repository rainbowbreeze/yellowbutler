from yellowbot.surfaces.baseinteractionsurface import BaseInteractionSurface


class FakeInteractionSurface(BaseInteractionSurface):
    """
    Surface to check if messages have really been sent
    Cannot call it TestInteractionSurface, otherwise tests will be execute
     on this class too
    """
    SURFACE_ID = "Test_Surface"
    RETURN_TEST = "Test performed"

    def __init__(self, surface_id):
        """
        Test surface

        :param surface_id: id of the surface to use
        :type surface_id: str
        """
        BaseInteractionSurface.__init__(self, surface_id)
        self.last_message = None

    def send_message(self, message):
        """Store the message received, and returns a specific string
        """

        self.last_message = message
        return self.RETURN_TEST

