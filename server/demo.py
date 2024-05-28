"""
Project name: Solstice
Description: Aruco tracking algorithm to determine whether UMats are worth
considering for April Tag tracking for the FIRST Robotics Competition.

Further reading: 
- https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html
"""

import multiprocessing
import cv2


from local import run_local
from webserver import run_webview

WEBVIEW: bool = False

def get_capture(
    index: int = 0, width: int = 1920, height: int = 1080, fps: int = 90
) -> cv2.VideoCapture:
    # Open basic video capture
    capture: cv2.VideoCapture = cv2.VideoCapture(index)

    # We should eventually have it use GStreamer, but this is not loading on my system
    # capture = cv2.VideoCapture("v4l2src device=dev/video0 ! image/jpeg,format=MJPG,width=1600,height=1200", cv2.CAP_GSTREAMER)

    # If we can't open video capture, immediately quit
    if not capture.isOpened():
        print("Cannot open capture at index ", index)
        exit(1)

    # Capture settings (ELP Camera testing)
    capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    capture.set(cv2.CAP_PROP_FPS, fps)

    return capture


def get_aruco_detector(dictionary: int = cv2.aruco.DICT_APRILTAG_36h11):
    aruco_dict = cv2.aruco.getPredefinedDictionary(dictionary)
    aruco_params = cv2.aruco.DetectorParameters()
    aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

    return aruco_detector


if __name__ == "__main__":
    capture: cv2.VideoCapture = get_capture(index=0, width=1920, height=1080, fps=90)
    capture3: cv2.VideoCapture = get_capture(index=6, width=1920, height=1080, fps=90)
    capture2: cv2.VideoCapture = get_capture(index=4, width=1600, height=1200, fps=50)
    aruco_detector: cv2.aruco.ArucoDetector = get_aruco_detector(
        dictionary=cv2.aruco.DICT_APRILTAG_16h5
    )

    processes = []

    if WEBVIEW:
        elp_process = multiprocessing.Process(target=run_webview, args=(capture, aruco_detector, 4451))
        arducam_process = multiprocessing.Process(target=run_webview, args=(capture2, aruco_detector, 4452))
        elp_process2 = multiprocessing.Process(target=run_webview, args=(capture3, aruco_detector, 4453))
    else:
        elp_process = multiprocessing.Process(target=run_local, args=(capture, aruco_detector, "ELP AR0234"))
        arducam_process = multiprocessing.Process(target=run_local, args=(capture2, aruco_detector, "Arducam OV2311"))
        elp_process2 = multiprocessing.Process(target=run_local, args=(capture3, aruco_detector, "ELP AR0234 WIDE"))

    processes.append(elp_process2)
    processes.append(elp_process)
    processes.append(arducam_process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    # Cleanup
    capture.release()
    capture2.release()
    capture3.release()
    cv2.destroyAllWindows()
