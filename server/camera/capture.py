from typing import Tuple

import cv2

from server.types import CameraConfig, MatLike


class Capture:
    """Interface for receiving Camera frames to use in other parts of the application."""

    def __init__(self):
        raise NotImplementedError

    def get_frame(self):
        raise NotImplementedError

    def release(self):
        raise NotImplementedError


class DefaultCapture(Capture):
    """This will have to work until we get GStreamer working"""

    def __init__(self, config: CameraConfig):
        self._config = CameraConfig

        self._video: cv2.VideoCapture = cv2.VideoCapture(config.v4l_index, cv2.CAP_V4L2)

        if not self._video.isOpened():
            print("Cannot open capture at index ", config.v4l_index)
            exit(1)

        # Capture settings
        self._video.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))  # type: ignore[reportAttributeAccessIssue]
        self._video.set(cv2.CAP_PROP_FRAME_WIDTH, config.width)
        self._video.set(cv2.CAP_PROP_FRAME_HEIGHT, config.height)
        self._video.set(cv2.CAP_PROP_FPS, config.fps)

    def get_frame(self) -> Tuple[bool, MatLike]:
        success, frame = self._video.read()
        return success, frame

    def release(self):
        self._video.release()
