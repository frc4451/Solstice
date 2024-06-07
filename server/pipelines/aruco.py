
from typing import Union
import cv2

from server.pipelines.fiducial_detection_pipeline import FiducialDetectionPipeline


class ArucoDetector(FiducialDetectionPipeline): 
    def __init__(self, dictionary: int = cv2.aruco.DICT_APRILTAG_36h11) -> None:
        self._dict = cv2.aruco.getPredefinedDictionary(dictionary)
        self._params = cv2.aruco.DetectorParameters()
        self._detector = cv2.aruco.ArucoDetector(self._dict, self._params)

    def detect(self, frame: Union[cv2.Mat, cv2.UMat], ) -> Union[cv2.Mat, cv2.UMat]:
        # Handle Aruco detection
        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = self.aruco_detector.detectMarkers(grayscale)

        if ids is not None:  # type: ignore[reportUnnecessaryComparison]
            # 2d marking
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        
        return frame