import cv2 
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class HandDetector:
    def __init__(
        self, 
        model_path, 
        max_hands=2,
        min_detection_confidence=0.5,
        min_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    ):
        self.model_path = model_path
        self.max_hands = max_hands
        self.min_detection_confidence = (min_detection_confidence)
        self.min_presence_confidence = (min_presence_confidence)
        self.min_tracking_confidence = (min_tracking_confidence)
        self.detector = None

    def open(self):
        base_options = python.BaseOptions(model_asset_path=self.model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=self.max_hands,
            min_hand_detection_confidence=(
                self.min_detection_confidence
            ),
            min_hand_presence_confidence=(
                self.min_presence_confidence
            ),
            min_tracking_confidence=(
                self.min_tracking_confidence
            ),
        )
        self.detector = (vision.HandLandmarker.create_from_options(options))

    def detect(self, frame, timestamp_ms):
        if self.detector is None:
            raise RuntimeError(
                "Detector is not open"
            )
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        result = self.detector.detect_for_video(mp_image, timestamp_ms)
        return result

    def close(self):
        if self.detector is not None:
            self.detector.close()
            self.detector = None