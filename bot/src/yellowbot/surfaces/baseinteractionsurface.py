"""
Base interaction surface, allow YellowBot to interact with the external
 world

A surface can be a chat app like Telegram, a textual console and much more
"""


class BaseInteractionSurface:
    """
    Define the basic methods and capabilities all interaction surfaces
     need to have
    """

    def __init__(self, surface_name):
        """

        :param surface_name: name of this interaction surface
        :type surface_name: str
        """
        self._surface_name = surface_name

    def send_message(self, message):
        """
        Send a message to the surface. Has to be implemented in derived
         classes

        :param message: a message to send
        :type message: SurfaceMessage

        :return: a string with something, if needed. In th future, it could be a status code or something else
        :rtype: str
        """
        raise ValueError("The surface {} cannot send a message".format(self._surface_name))
