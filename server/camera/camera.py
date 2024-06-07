import multiprocessing
from server.camera.capture import DefaultCapture
from server.output.webserver import VideoWebServer
from server.pipelines.fiducial_pipeline import FiducialPipeline
from server.types import CameraConfig, MatLike


class Camera:
    def __init__(self, config: CameraConfig) -> None:
        self.config: CameraConfig = config
        self.detector: FiducialPipeline = config.detection_pipeline
        self.capture = DefaultCapture(config=config)
        self.webserver = VideoWebServer(tab_title=config.custom_user_id)
        self.process = multiprocessing.Process(target=self._run_process)
    
        self.process.start()

    def _run_process(self):
        print("amogus")
        frame: MatLike = self.capture.get_frame()
        # frame = self.detector.detect(frame)
        # self.webserver.set_frame(frame)

    def terminate(self) -> None:
        self.process.terminate()
        self.capture.release()
