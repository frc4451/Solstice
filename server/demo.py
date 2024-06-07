"""
Project name: Solstice
Description: Aruco tracking algorithm to determine whether UMats are worth
considering for April Tag tracking for the FIRST Robotics Competition.

Further reading: 
- https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html
"""

import cv2

# import ntcore
from server.camera.camera_manager import CameraManager
from server.types import CameraConfig

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

    if cv2.cuda.getCudaEnabledDeviceCount() > 1:
        print("CUDA IS ALLOWED")

    return capture


if __name__ == "__main__":
    camera_manager = CameraManager()

    camera_manager.load_camera_config(
        CameraConfig(
            "ELP AR0234",
            8080,
            0,
            1920,
            1080,
            90,
            cv2.aruco.DICT_APRILTAG_16h5,
        )
    )

    camera_manager.load_camera_config(
        CameraConfig(
            "Arducam OV2311",
            8082,
            2,
            1600,
            1200,
            90,
            cv2.aruco.DICT_APRILTAG_16h5,
        )
    )

    # nt_root = "/Solstice"
    # nt = ntcore.NetworkTableInstance.getDefault()
    # nt.startClient4("Solstice")
    # nt.setServerTeam(TEAM)
    # nt.setServer("localhost", ntcore.NetworkTableInstance.kDefaultPort4)
    # nt.startServer()

    # n_topic = nt.getIntegerTopic(nt_root + "/among")

    # n_publisher = n_topic.publish()

    # n_publisher.setDefault(0)
    # n_publisher.set(69)

    # print(n_topic.getEntry(0).get())

    try:
        camera_manager.wait_for_proccesses()
    finally:
        camera_manager.terminate_all()
