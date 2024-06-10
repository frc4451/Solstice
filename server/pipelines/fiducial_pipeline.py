from abc import ABC, abstractmethod

from cv2.typing import MatLike


class FiducialPipeline(ABC):
    """Abstract for any form of fiducial detection pipelines (April Tags, Object, etc)"""

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def process(self, frame: MatLike) -> MatLike:
        pass
