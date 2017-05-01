"""
Main class
"""


class YellowButler:
    """
    The main Yellow Butler class.
    It should be the entry-point for everything
    """

    def __init__(self):
        # Registers all the allowed keys
        self.keys = []
        # TODO: Registers Yellow Butler modules to add features

    def echo_message(self, key, message):
        """Echo a simple message"""
        # if not self.is_security_code_valid(key):
        #     return self.unauthorize_answer(key)
        return 'You said: {}'.format(message)

    def append_security_key(self, new_key):
        """Add a new security key to the allowed ones"""
        self.keys.append(new_key)

    def is_security_code_valid(self, security_code):
        try:
            self.keys.index(security_code)
            return True
        except ValueError:
            return False

    def unauthorize_answer(self, key):
        print("Attempt to access with a wrong key {}".format(key))
        return 404
