import multiprocessing
from typing import NoReturn

import cv2
from mjpeg_streamer.server import Server  # type: ignore[reportMissingTypeStubs]
from mjpeg_streamer.stream import Stream  # type: ignore[reportMissingTypeStubs]

from server.camera.capture import DefaultCapture
from server.pipelines.fiducial_pipeline import FiducialPipeline
from server.types import CameraConfig


class Camera:
    def __init__(self, config: CameraConfig) -> None:
        self.config: CameraConfig = config
        self.detector: FiducialPipeline = config.detection_pipeline
        self.capture = DefaultCapture(config)
        self.server = Server(["localhost", "0.0.0.0"], config.web_port)
        self.raw_stream = Stream(
            name=config.custom_user_id + "_raw",
            fps=config.fps,
            size=(config.height, config.width),
            quality=50,
        )
        self.processed_stream = Stream(
            name=config.custom_user_id + "_processed",
            fps=config.fps,
            size=(config.height, config.width),
            quality=50,
        )
        self.process = multiprocessing.Process(target=self._run_process)

        self.process.start()

    def _run_process(self) -> NoReturn:
        self.server.add_stream(self.raw_stream)
        self.server.add_stream(self.processed_stream)
        self.server.start()

        while True:
            _, raw_frame = self.capture.get_frame()
            mat_frame = cv2.UMat(raw_frame)  # type: ignore[reportArgumentType]
            processed_frame = self.detector.process(mat_frame)
            self.raw_stream.set_frame(mat_frame)  # type: ignore[reportArgumentType]
            self.processed_stream.set_frame(processed_frame)  # type: ignore[reportArgumentType]

    def terminate(self) -> None:
        self.server.stop()
        self.process.terminate()
        self.capture.release()
