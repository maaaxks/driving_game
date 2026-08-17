import time

from vision.camera import Camera
from vision.hand_detector import HandDetector
from vision.gestures import GestureAnalyzer


class VisionManager:

    def __init__(
        self,
        model_path="models/vision/hand_landmarker.task",
        camera_index=0,
        camera_width=640,
        camera_height=480,
    ):

        self.camera = Camera(
            camera_index=camera_index,
            width=camera_width,
            height=camera_height,
        )

        self.detector = HandDetector(
            model_path=model_path,
            max_hands=2,
            min_detection_confidence=0.5,
            min_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )

        self.gestures = GestureAnalyzer()
        self.timestamp_ms = 0
        self.last_time = time.perf_counter()
        self.fps = 0.0

    def start(self):

        self.camera.open()
        self.detector.open()
        self.timestamp_ms = 0
        self.last_time = (time.perf_counter())

    def update(self):

        frame = self.camera.read()
        if frame is None:
            return None, None

        current_time = time.perf_counter()
        dt = current_time - self.last_time
        self.last_time = current_time

        if dt > 0:
            instant_fps = 1.0 / dt
            self.fps = (self.fps * 0.9 + instant_fps * 0.1)

        self.timestamp_ms += max(1, int(dt * 1000))
        result = self.detector.detect(frame, self.timestamp_ms)
        hands = []

        for index, landmarks in enumerate(result.hand_landmarks):
            handedness = "Unknown"

            if (index < len(result.handedness) and result.handedness[index]):
                handedness = (result.handedness[index][0].category_name)
            hands.append(
                {
                    "handedness": handedness,
                    "landmarks": landmarks,
                }
            )

        height, width = frame.shape[:2]
        state = self.gestures.analyze(
            hands,
            width,
            height,
        )

        return frame, state

    def stop(self):

        self.detector.close()
        self.camera.release()