class FiducialPipeline:
    """Abstract for any form of fiducial detection pipelines (April Tags, Object, etc)"""

    def __init__(self):
        raise NotImplementedError

    def detect(self, frame):
        raise NotImplementedError
