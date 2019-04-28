from yellowbot.surfaces.notifyadminsurface import NotifyAdminSurface


class FakeNotifyAdminInteractionSurface(NotifyAdminSurface):
    """
    Surface to check if messages have really been sent
    Cannot call it TestInteractionSurface, otherwise tests will be execute
     on this class too
    """
    RETURN_TEST = "Test Notify Admin"

    def __init__(self, surface_id, channel_id):
        """
        Test surface

        :param surface_id: id of the surface to use
        :type surface_id: str
        """
        NotifyAdminSurface.__init__(self, surface_id, channel_id)
        self.last_message = None

    def send_message(self, message):
        self.last_message = message
        return self.RETURN_TEST
