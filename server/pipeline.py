# from math import ceil
# import time

# import cv2


# class ArucoPipeline:
#     def __init__():
#         pass

#     def run_aruco_pipeline(self):
#         while True:
#             start_time = time.time()
#             success, frame = self.capture.read(image=cv2.UMat())
#             if not success:
#                 break

#             frame = cv2.UMat(frame)

#             # Handle Aruco detection
#             grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             corners, ids, _ = self.aruco_detector.detectMarkers(grayscale)

#             if ids is not None:  # type: ignore[reportUnnecessaryComparison]
#                 # 2d marking
#                 cv2.aruco.drawDetectedMarkers(frame, corners, ids)

#             # Diagnostic information
#             fps: int = ceil((time.time() - start_time) ** -1)
#             width: int = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
#             height: int = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

#             cv2.putText(
#                 frame,
#                 f"{width} x {height}",
#                 (10, 20),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.7,
#                 (0, 255, 0),
#                 1,
#             )

#             cv2.putText(
#                 frame,
#                 f"FPS: {fps}",
#                 (10, 40),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.7,
#                 (0, 255, 0),
#                 1,
#             )
