"""
Project name: Solstice
Description: Aruco tracking algorithm to determine whether UMats are worth
considering for April Tag tracking for the FIRST Robotics Competition.

Further reading: 
- https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html
"""

import cv2

import time

import numpy as np

if __name__ == "__main__":
    # Open basic video capture
    capture: cv2.VideoCapture = cv2.VideoCapture(0)

    # We should eventually have it use GStreamer, but this is not loading on my system
    # capture = cv2.VideoCapture("v4l2src device=dev/video0 ! image/jpeg,format=MJPG,width=1600,height=1200", cv2.CAP_GSTREAMER)

    # If we can't open video capture, immediately quit
    if not capture.isOpened():
        print("Cannot open capture")
        exit(1)

    ### Aruco settings
    # I have 16h5 mounted in my office, but this will be 36h11 in competition
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_16h5)
    aruco_params = cv2.aruco.DetectorParameters()
    aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

    # Capture settings (ELP Camera testing)
    capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    capture.set(cv2.CAP_PROP_FPS, 90)

    # Capture settings (Arducam OV2311 Camera testing)
    # capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    # capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
    # capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
    # capture.set(cv2.CAP_PROP_FPS, 50)

    # Infinite loop to see camera
    while True:
        start_time = time.time()
        success, frame = capture.read()

        # This puts the data in GPU memory to help keep steady frames
        # From testing with a 3060, this actually reduces our reported
        # FPS on the camera. Maybe we can read directly as UMat?
        # frame = cv2.UMat(frame)

        if not success:
            print("Error reading frame")
            break

        # Handle Aruco detection
        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = aruco_detector.detectMarkers(grayscale)

        if ids is not None:
            # 2d marking
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # Diagnostic information
        fps: float = 1 / (time.time() - start_time)
        width: int = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height: int = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        cv2.putText(
            frame,
            f"{width} x {height}",
            (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            1,
        )

        cv2.putText(
            frame,
            f"FPS: {fps}",
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            1,
        )

        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Cleanup
    capture.release()
    cv2.destroyAllWindows()
