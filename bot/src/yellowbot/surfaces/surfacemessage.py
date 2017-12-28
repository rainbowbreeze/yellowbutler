"""

"""


class SurfaceMessage:
    """
    Represents a message that can be sent thru an interaction surface
    """

    def __init__(self, surface_id, channel_id, text):
        """
        Creates a new message

        :param surface_id: the surface name originating the message
        :type surface_id: str

        :param channel_id: the channel_id where to send the message, if any
        :type channel_id: str

        :param text: the text to send
        :type text: str
        """
        self.surface_id = surface_id
        self.channel_id = channel_id
        self.text = text
