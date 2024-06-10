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
from server.pipelines.aruco import ArucoDetectionPipeline
from server.types import CameraConfig

TEAM = 4451


if __name__ == "__main__":
    camera_manager = CameraManager()

    camera_manager.load_camera_config(
        CameraConfig(
            custom_user_id="ELP AR0234",
            web_port=8080,
            v4l_index=1,
            height=1920,
            width=1080,
            fps=90,
            detection_pipeline=ArucoDetectionPipeline(dictionary=cv2.aruco.DICT_APRILTAG_16h5),
        )
    )

    # camera_manager.load_camera_config(
    #     CameraConfig(
    #         "Arducam OV2311",
    #         8082,
    #         2,
    #         1600,
    #         1200,
    #         90,
    #         cv2.aruco.DICT_APRILTAG_16h5,
    #     )
    # )

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
