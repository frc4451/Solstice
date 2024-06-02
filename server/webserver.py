import http.server
import socketserver
import time
from math import ceil

import cv2


class VideoWebServer(http.server.BaseHTTPRequestHandler):
    def __init__(
        self,
        capture: cv2.VideoCapture,
        aruco_detector: cv2.aruco.ArucoDetector,
        tab_title: str,
        *args,
        **kwargs,
    ):
        self.capture = capture
        self.aruco_detector = aruco_detector
        self.tab_title = tab_title
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            # someone smarter than me figure this out
            # self.send_header("Content-Type", f'text/html; title="${self.tab_title}"')
            self.send_header(
                "Content-type", "multipart/x-mixed-replace; boundary=--frame"
            )
            self.end_headers()
            while True:
                start_time = time.time()
                success, frame = self.capture.read()
                if not success:
                    break

                # Handle Aruco detection
                grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                corners, ids, _ = self.aruco_detector.detectMarkers(grayscale)

                if ids is not None:  # type: ignore[reportUnnecessaryComparison]
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

                _, buffer = cv2.imencode(".jpg", frame)
                frame = buffer.tobytes()
                self.wfile.write(b"--frame\r\n")
                self.wfile.write(b"Content-Type: image/jpeg\r\n\r\n")
                self.wfile.write(frame)
                self.wfile.write(b"\r\n")
        else:
            self.send_error(404)


def run_webview(
    capture: cv2.VideoCapture,
    aruco_detector: cv2.aruco.ArucoDetector,
    port: int = 4451,
    custom_user_id: str = "Solstice",
) -> None:
    # allow the socket to be immediately reused https://stackoverflow.com/a/27360648
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(
        ("", port),
        lambda *args, **kwargs: VideoWebServer(
            capture, aruco_detector, custom_user_id, *args, **kwargs
        ),
    ) as tcp_server:
        print("Server started at localhost:" + str(port))
        tcp_server.serve_forever()
