from server.types import CameraConfig


class Capture:
    """Interface for receiving Camera frames to use in other parts of the application."""
    def __init__(self):
        raise NotImplementedError
    

class DefaultCapture(Capture):
    """This will have to work until we get GStreamer working"""

    def __init__(self):
        pass

    _video = None
    _config = CameraConfig