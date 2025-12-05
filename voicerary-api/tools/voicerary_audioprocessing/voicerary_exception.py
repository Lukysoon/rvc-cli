class VoiceraryException(Exception):
    def __init__(self, log_message: str, user_message: str, orig_traceback: list = None):
        super().__init__(log_message)
        self.user_message = user_message
        self.orig_traceback = orig_traceback
