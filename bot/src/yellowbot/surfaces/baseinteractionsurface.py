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
        """
        self._surface_name = surface_name

    def send_message(self, message):
        """
        Send a message to the surface. Has to be implemented in derived
         classes

        :param message: a SurfaceMessage to send
        :return:
        """
        raise ValueError("The surface {} cannot send a message".format(self._surface_name))

    def can_handle_surface(self, surface_id):
        """
        Check if this surface can handle messages directed to a given surface
        :param surface_id: the target surface id
        :return: True if the surface is able, otherwise false
        """
        return surface_id == self._surface_name