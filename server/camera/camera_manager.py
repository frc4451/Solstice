from server.camera.camera import Camera
from server.camera.types import CameraConfig


class CameraManager:
    def __init__(self) -> None:
        self.cameras: dict[str, Camera] = {}

    def load_camera_config(self, camera_config: CameraConfig) -> None:
        camera_to_update = self.cameras.get(camera_config.custom_user_id)
        if camera_to_update != None:
            camera_to_update.terminate()

        self.cameras[camera_config.custom_user_id] = Camera(camera_config)

    def terminate_all(self) -> None:
        for camera in self.cameras.values():
            camera.terminate()

    def wait_for_proccesses(self) -> None:
        for camera in self.cameras.values():
            camera.process.join()

        # In case more proccesses have been added we need to check again
        if len(self.cameras.values()) > 0:
            self.wait_for_proccesses()