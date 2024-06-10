from abc import ABC, abstractmethod
from typing import override

import cv2
from cv2.typing import MatLike

from server.types import CameraConfig


class Capture(ABC):
    """Interface for receiving Camera frames to use in other parts of the application."""

    @abstractmethod
    def get_frame(self) -> tuple[bool, MatLike]:
        pass

    @abstractmethod
    def release(self) -> None:
        raise NotImplementedError


class DefaultCapture(Capture):
    """This will have to work until we get GStreamer working"""

    def __init__(self, config: CameraConfig) -> None:
        self._config = CameraConfig

        self._video = cv2.VideoCapture(config.v4l_index, cv2.CAP_V4L2)

        if not self._video.isOpened():
            print("Cannot open capture at index ", config.v4l_index)
            exit(1)

        # Capture settings
        self._video.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))  # type: ignore[reportAttributeAccessIssue]
        self._video.set(cv2.CAP_PROP_FRAME_WIDTH, config.width)
        self._video.set(cv2.CAP_PROP_FRAME_HEIGHT, config.height)
        self._video.set(cv2.CAP_PROP_FPS, config.fps)

    @override
    def get_frame(self) -> tuple[bool, MatLike]:
        success, frame = self._video.read()
        return success, frame

    @override
    def release(self) -> None:
        self._video.release()
