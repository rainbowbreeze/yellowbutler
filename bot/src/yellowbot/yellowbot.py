"""
Main class
"""

class YellowBot:
    """
    Entry point for the bot
    """

    def __init__(self):
        self.keys = []
        self.module = []

    def echo_message(self, message):
        return "You said {}".format(message)

    def is_security_code_valid(self, security_code):
        try:
            self.keys.index(security_code)
            return True
        except ValueError:
            return False

    def unauthorize_answer(self, key):
        print("Attempt to access with a wrong key {}".format(key))
        return 404
    