from time import sleep

from server.camera.camera import Camera
from server.types import CameraConfig


class CameraManager:
    def __init__(self) -> None:
        self.cameras: dict[str, Camera] = {}

    def load_camera_config(self, camera_config: CameraConfig) -> None:
        old_camera = self.cameras.get(camera_config.custom_user_id)
        if old_camera != None:
            old_camera.terminate()
            # make sure the old capture is able to be released before we start trying to possibly use it again
            sleep(0.1)

        self.cameras[camera_config.custom_user_id] = Camera(camera_config)

    def terminate_all(self) -> None:
        for camera in self.cameras.values():
            camera.terminate()

    def wait_for_proccesses(self) -> None:
        # Check if *any* processes are alive
        # If so wait for that *one*
        # Then check again
        # Once none are alive we can finally end this recursive calling
        for camera in self.cameras.values():
            if camera.process.is_alive():
                camera.process.join()
                return self.wait_for_proccesses()
