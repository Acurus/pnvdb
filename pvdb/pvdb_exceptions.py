class NvdbError(Exception):
    """Base class for exceptions in this module."""
    pass

class ResponseError(NvdbError):
    def __init__(self,message):
        self.message = message