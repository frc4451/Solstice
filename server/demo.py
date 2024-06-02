"""
Project name: Solstice
Description: Aruco tracking algorithm to determine whether UMats are worth
considering for April Tag tracking for the FIRST Robotics Competition.

Further reading: 
- https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html
"""

import multiprocessing
from dataclasses import dataclass

import cv2
import ntcore
from local import run_local

# from webserver import run_webview

TEAM = 4451
WEBVIEW = False


def get_capture(
    index: int = 0, width: int = 1920, height: int = 1080, fps: int = 90
) -> cv2.VideoCapture:
    # Open basic video capture
    capture: cv2.VideoCapture = cv2.VideoCapture(index, cv2.CAP_V4L2)

    # We should eventually have it use GStreamer, but this is not loading on my system
    # capture = cv2.VideoCapture("v4l2src device=dev/video0 ! image/jpeg,format=MJPG,width=1600,height=1200", cv2.CAP_GSTREAMER)

    # If we can't open video capture, immediately quit
    if not capture.isOpened():
        print("Cannot open capture at index ", index)
        exit(1)

    # Capture settings (ELP Camera testing)
    capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))  # type: ignore[reportAttributeAccessIssue]
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    capture.set(cv2.CAP_PROP_FPS, fps)

    return capture


def get_aruco_detector(
    dictionary: int = cv2.aruco.DICT_APRILTAG_36h11,
) -> cv2.aruco.ArucoDetector:
    aruco_dict = cv2.aruco.getPredefinedDictionary(dictionary)
    aruco_params = cv2.aruco.DetectorParameters()
    aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

    return aruco_detector


class Camera:
    capture: cv2.VideoCapture
    proccess: multiprocessing.Process

    def __init__(
        self, capture: cv2.VideoCapture, proccess: multiprocessing.Process
    ) -> None:
        self.capture = capture
        self.proccess = proccess
        self.proccess.start()

    def terminate(self) -> None:
        self.proccess.terminate()
        self.capture.release()


@dataclass
class CameraConfig:
    custom_user_id: str
    v4l_index: int
    width: int
    height: int
    fps: int
    aruco_dict: int


class CameraManager:
    def __init__(self) -> None:
        self.cameras: dict[str, Camera] = {}

    def load_camera_config(self, camera_config: CameraConfig) -> None:
        camera_to_update = self.cameras.get(camera_config.custom_user_id)
        if camera_to_update != None:
            camera_to_update.terminate()

        capture = get_capture(
            index=camera_config.v4l_index,
            width=camera_config.width,
            height=camera_config.height,
            fps=camera_config.fps,
        )

        aruco_detector = get_aruco_detector(camera_config.aruco_dict)

        process = multiprocessing.Process(
            target=run_local,
            args=(capture, aruco_detector, camera_config.custom_user_id),
        )

        self.cameras[camera_config.custom_user_id] = Camera(capture, process)

    def terminate_all(self) -> None:
        for camera in self.cameras.values():
            camera.terminate()

    def wait_for_proccesses(self) -> None:
        for camera in self.cameras.values():
            camera.proccess.join()


if __name__ == "__main__":
    camera_manager = CameraManager()

    camera_manager.load_camera_config(
        CameraConfig(
            "my_epic_webcam",
            0,
            1920,
            1080,
            30,
            cv2.aruco.DICT_APRILTAG_16h5,
        )
    )

    nt = ntcore.NetworkTableInstance.create()
    nt.setServerTeam(TEAM, 2017)

    # if WEBVIEW:
    #     elp_process = multiprocessing.Process(
    #         target=run_webview, args=(capture, aruco_detector, 4451)
    #     )
    # else:
    #     elp_process = multiprocessing.Process(
    #         target=run_local, args=(capture, aruco_detector, "ELP AR0234")
    #     )

    try:
        camera_manager.wait_for_proccesses()
    finally:
        camera_manager.terminate_all()
