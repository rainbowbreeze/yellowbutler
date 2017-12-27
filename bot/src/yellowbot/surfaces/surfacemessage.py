"""

"""


class SurfaceMessage:
    """
    Represents a message that can be sent thru an interaction surface
    """

    def __init__(self, channel_id, text):
        """
        Creates a new message

        :param channel_id: the channel_id where to send the message, if any
        :param text: the text to send
        """
        self.channel_id = channel_id
        self.text = text
