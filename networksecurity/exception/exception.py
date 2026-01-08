import sys
class NetworkSecurityLoggingException(Exception):
    """Base exception for network security logging errors."""
    def __init__(self, message="An error occurred in network security logging."):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"NetworkSecurityLoggingException: {self.message}"

    def log_exception(self):
        """Logs the exception details to stderr."""
        print(f"ERROR: {self.message}", file=sys.stderr)    



