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
from webserver import run_webview

TEAM = 4451


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


@dataclass
class CameraConfig:
    custom_user_id: str
    web_port: int
    v4l_index: int
    width: int
    height: int
    fps: int
    aruco_dict: int


class Camera:
    def __init__(self, config: CameraConfig) -> None:
        self.config = config

        self.aruco_detector = get_aruco_detector(config.aruco_dict)

        self.capture = get_capture(
            index=config.v4l_index,
            width=config.width,
            height=config.height,
            fps=config.fps,
        )

        self.process = multiprocessing.Process(
            target=run_webview,
            args=(
                self.capture,
                self.aruco_detector,
                config.web_port,
                config.custom_user_id,
            ),
        )

        self.process.start()

    def terminate(self) -> None:
        self.process.terminate()
        self.capture.release()


class CameraManager:
    def __init__(self) -> None:
        self.cameras: dict[str, Camera] = {}

    def load_camera_config(self, camera_config: CameraConfig) -> None:
        camera_to_update = self.cameras.get(camera_config.custom_user_id)
        if camera_to_update != None:
            camera_to_update.terminate()

        self.cameras[camera_config.custom_user_id] = Camera(camera_config)

    def terminate_all(self) -> None:
        for camera in self.cameras.values():
            camera.terminate()

    def wait_for_proccesses(self) -> None:
        for camera in self.cameras.values():
            camera.process.join()

        # In case more proccesses have been added we need to check again
        if len(self.cameras.values()) > 0:
            self.wait_for_proccesses()


if __name__ == "__main__":
    camera_manager = CameraManager()

    camera_manager.load_camera_config(
        CameraConfig(
            "my_epic_webcam",
            8080,
            0,
            1920,
            1080,
            30,
            cv2.aruco.DICT_APRILTAG_16h5,
        )
    )

    nt_root = "/Solstice"
    nt = ntcore.NetworkTableInstance.getDefault()
    nt.startClient4("Solstice")
    nt.setServerTeam(TEAM)
    nt.setServer("localhost", ntcore.NetworkTableInstance.kDefaultPort4)
    nt.startServer()

    n_topic = nt.getIntegerTopic(nt_root + "/among")

    n_publisher = n_topic.publish()

    n_publisher.setDefault(0)
    n_publisher.set(69)

    print(n_topic.getEntry(0).get())

    try:
        camera_manager.wait_for_proccesses()
    finally:
        camera_manager.terminate_all()
