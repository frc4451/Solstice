import time
from math import ceil

import cv2


def run_local(
    capture: cv2.VideoCapture,
    aruco_detector: cv2.aruco.ArucoDetector,
    label: str = "Frame",
) -> None:
    # Infinite loop to see camera
    while True:
        start_time = time.time()
        success, frame = capture.read()

        if not success:
            print("Error reading frame")
            break

        # This puts the data in GPU memory to help keep steady frames
        # From testing with a 3060, this actually reduces our reported
        # FPS on the camera. Maybe we can read directly as UMat?
        # if UMAT:
        #     frame = cv2.UMat(frame)

        # Handle Aruco detection
        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = aruco_detector.detectMarkers(grayscale)

        if ids.size > 0:
            # 2d marking
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # Diagnostic information
        fps: int = ceil((time.time() - start_time) ** -1)
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

        cv2.imshow(label, frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
