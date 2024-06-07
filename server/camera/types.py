from dataclasses import dataclass


@dataclass
class CameraConfig:
    custom_user_id: str
    web_port: int
    v4l_index: int
    width: int
    height: int
    fps: int
    aruco_dict: int