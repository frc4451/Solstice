from dataclasses import dataclass

from server.pipelines.fiducial_pipeline import FiducialPipeline


@dataclass
class CameraConfig:
    custom_user_id: str
    web_port: int
    v4l_index: int
    width: int
    height: int
    fps: int
    detection_pipeline: FiducialPipeline
