import cv2

from typing import Union
from dataclasses import dataclass

from server.pipelines.fiducial_pipeline import FiducialPipeline

MatLike = Union[cv2.Mat, cv2.UMat]
"""Could be either Mat, or UMat. But not GMat."""


@dataclass
class CameraConfig:
    custom_user_id: str
    web_port: int
    v4l_index: int
    width: int
    height: int
    fps: int
    detection_pipeline: FiducialPipeline
