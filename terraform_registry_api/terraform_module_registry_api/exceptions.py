
class ModuleNotFoundException(Exception):
    """ModuleNotFoundException.

    An Exception thrown when a module was requested that was not found
    in the configured backend
    """

    def __init__(self, message):
        """Initialize the Exception.

        Args:
            message (str): Description of the exception cause
        """
        self.message = message
        super().__init__(self.message)


class FileNotFoundException(Exception):
    """FileNotFoundException.

    An Exception thrown when a file from a module was requested that
    was not found in the configured backend
    """

    def __init__(self, message):
        """Initialize the Exception.

        Args:
            message (str): Description of the exception cause
        """
        self.message = message
        super().__init__(self.message)
