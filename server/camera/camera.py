
from server.pipelines.aruco import ArucoDetector
from server.types import CameraConfig


class Camera:
    def __init__(self, config: CameraConfig) -> None:
        self.config = config

        self.aruco_detector = ArucoDetector.get_aruco_detector(config.aruco_dict)

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