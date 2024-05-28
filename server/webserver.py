from math import ceil
import threading
import time
import cv2
import numpy as np
import http.server
import socketserver

class VideoWebServer(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, capture: cv2.VideoCapture, aruco_detector: cv2.aruco.ArucoDetector, **kwargs):
        self.capture = capture
        self.aruco_detector = aruco_detector
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--frame')
            self.end_headers()
            try:
                while True:
                    start_time = time.time()
                    success, frame = self.capture.read()
                    if not success:
                        break

                    # Handle Aruco detection
                    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    corners, ids, _ = self.aruco_detector.detectMarkers(grayscale)

                    if ids is not None:
                        # 2d marking
                        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

                    # Diagnostic information
                    fps: int = ceil((time.time() - start_time) ** -1)
                    width: int = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height: int = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

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

                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    self.wfile.write(b'--frame\r\n')
                    self.wfile.write(b'Content-Type: image/jpeg\r\n\r\n')
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            finally:
                self.capture.release()
        else:
            self.send_error(404)


def run_webview(capture: cv2.VideoCapture, aruco_detector: cv2.aruco.ArucoDetector, port: int = 4451):
        try:
            with socketserver.TCPServer(
                ("", port),
                lambda *args, **kwargs: VideoWebServer(
                    *args, capture=capture, aruco_detector=aruco_detector, **kwargs
                ),
            ) as httpd:
                print("Server started at localhost:" + str(port))
                httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
            print("Server stopped")
        finally:
            httpd.server_close()