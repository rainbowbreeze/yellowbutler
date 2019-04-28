"""

"""


class SurfaceMessage:
    """
    Represents a message that can be sent through an interaction surface
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
        # str() because can arrive something different from a string
        self.surface_id = self._none_if_emtpy_otherwise_value(surface_id)
        self.channel_id = self._none_if_emtpy_otherwise_value(channel_id)
        self.text = self._none_if_emtpy_otherwise_value(text)

    def _none_if_emtpy_otherwise_value(self, string):
        """
        Return None if the string is None or empty or full of spaces, otherwise
         the string value

        Based on https://stackoverflow.com/a/24534152

        :param string: the string to check
        :return string: str
        """

        # Check for strip() to a non str object raises and error, so the check
        #  on the type before everything else
        if string is None:
            return None
        elif isinstance(string, str):
            # Check for empty string of None of full of spaces
            return None if not (string and string.strip()) else string
        else:
            # Convert to a string and return
            return str(string)
