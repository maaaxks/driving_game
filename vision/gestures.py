import math
from dataclasses import dataclass
from typing import Optional

@dataclass
class HandData:
    handedness: str
    landmarks: list

    # wrist coord
    wrist_x: float
    wrist_y: float

    # palm center 
    center_x: float
    center_y: float

    # palm size
    palm_size: float

    # hand condition
    is_fist: bool
    is_open: bool

@dataclass
class VisionState:

    left_hand: Optional[HandData] = None
    right_hand: Optional[HandData] = None

    hands_visible: bool = False

    steering_angle: float = 0.0

    steering: float = 0.0

    wheel_center_x: float = 0.0
    wheel_center_y: float = 0.0

    wheel_radius: float = 0.0

    gas: float = 0.0
    brake: float = 0.0

    left_fist: bool = False
    right_fist: bool = False

    left_open: bool = False
    right_open: bool = False


class GestureAnalyzer:

    WRIST = 0

    THUMB_CMC = 1
    THUMB_MCP = 2
    THUMB_IP = 3
    THUMB_TIP = 4

    INDEX_MCP = 5
    INDEX_PIP = 6
    INDEX_DIP = 7
    INDEX_TIP = 8

    MIDDLE_MCP = 9
    MIDDLE_PIP = 10
    MIDDLE_DIP = 11
    MIDDLE_TIP = 12

    RING_MCP = 13
    RING_PIP = 14
    RING_DIP = 15
    RING_TIP = 16

    PINKY_MCP = 17
    PINKY_PIP = 18
    PINKY_DIP = 19
    PINKY_TIP = 20

    def __init__(self, max_steering_angle=45.0):

        self.max_steering_angle = max_steering_angle
    @staticmethod
    def distance(a, b):

        dx=a.x-b.x
        dy=a.y-b.y
        return math.sqrt(dx * dx + dy * dy)

    @staticmethod
    def pixel_distance(a, b):

        dx = a[0] - b[0]
        dy = a[1] - b[1]
        return math.sqrt(dx * dx + dy * dy)

    def calculate_palm_size(self, landmarks):

        wrist = landmarks[self.WRIST]
        middle_mcp = landmarks[self.MIDDLE_MCP]
        return self.distance(wrist, middle_mcp)

    def is_fist(self, landmarks):
        wrist = landmarks[self.WRIST]
        palm_size = self.calculate_palm_size(landmarks)
        if palm_size < 0.001:
            return False

        fingertips = [
            self.INDEX_TIP,
            self.MIDDLE_TIP,
            self.RING_TIP,
            self.PINKY_TIP,
        ]

        finger_pips = [
            self.INDEX_PIP,
            self.MIDDLE_PIP,
            self.RING_PIP,
            self.PINKY_PIP,
        ]
        tip_distances = []
        pip_distances = []

        for tip_index in fingertips:
            distance = self.distance(landmarks[tip_index], wrist)
            tip_distances.append(distance / palm_size)

        for pip_index in finger_pips:
            distance = self.distance(landmarks[pip_index], wrist)
            pip_distances.append(distance / palm_size)

        folded_fingers = 0
        for tip_distance, pip_distance in zip(tip_distances, pip_distances):
            if tip_distance < pip_distance * 1.15:
                folded_fingers += 1

        return folded_fingers >= 3

    def is_open_palm(self, landmarks):

        wrist=landmarks[self.WRIST]
        palm_size=self.calculate_palm_size(landmarks)
        if palm_size<0.001:
            return False
        
        fingertips = [
                    self.INDEX_TIP,
                    self.MIDDLE_TIP,
                    self.RING_TIP,
                    self.PINKY_TIP,
                ]
        
        finger_pips = [
            self.INDEX_PIP,
            self.MIDDLE_PIP,
            self.RING_PIP,
            self.PINKY_PIP,
        ]

        extended_fingers = 0
        for tip_index, pip_index in zip(fingertips, finger_pips):
            tip_distance = self.distance(landmarks[tip_index], wrist)
            pip_distance = self.distance(landmarks[pip_index], wrist)
            if tip_distance > pip_distance * 1.25:
                extended_fingers += 1

        return extended_fingers >= 3

    def create_hand_data(self, handedness, landmarks, frame_width, frame_height):

        wrist = landmarks[self.WRIST]

        wrist_x = wrist.x * frame_width
        wrist_y = wrist.y * frame_height

        center_indices = [
            self.WRIST,
            self.INDEX_MCP,
            self.MIDDLE_MCP,
            self.RING_MCP,
            self.PINKY_MCP,
        ]

        center_x = sum(landmarks[index].x for index in center_indices) / len(center_indices)
        center_y = sum(landmarks[index].y for index in center_indices) / len(center_indices)

        center_x *= frame_width
        center_y *= frame_height

        palm_size = (self.calculate_palm_size(landmarks) * frame_width)
        fist = self.is_fist(landmarks)
        open_palm = self.is_open_palm(landmarks)

        return HandData(
            handedness=handedness,
            landmarks=landmarks,
            wrist_x=wrist_x,
            wrist_y=wrist_y,
            center_x=center_x,
            center_y=center_y,
            palm_size=palm_size,
            is_fist=fist,
            is_open=open_palm,
        )

    def calculate_steering(self, left_hand, right_hand):
        dx = (right_hand.wrist_x - left_hand.wrist_x)
        dy = (right_hand.wrist_y - left_hand.wrist_y)

        if abs(dx) < 1.0 and abs(dy) < 1.0:
            return 0.0, 0.0

        angle = math.degrees(math.atan2(-dy, dx))

        if angle > 90:
            angle -= 180

        if angle < -90:
            angle += 180

        steering = (angle / self.max_steering_angle)
        steering = max(-1.0, min(1.0, steering))
        return angle, steering

    def analyze(self, hands, frame_width, frame_height):

        state = VisionState()
        if not hands:
            return state

        detected_hands = []

        for hand_info in hands:
            detected_hands.append(
                self.create_hand_data(
                    hand_info["handedness"],
                    hand_info["landmarks"],
                    frame_width,
                    frame_height,
                )
            )

        for hand in detected_hands:
            if hand.handedness == "Left":
                state.left_hand = hand

            elif hand.handedness == "Right":
                state.right_hand = hand

        state.hands_visible = (state.left_hand is not None or state.right_hand is not None)

        if (state.left_hand is not None and state.right_hand is not None):

            angle, steering = (
                self.calculate_steering(
                    state.left_hand,
                    state.right_hand,
                )
            )

            state.steering_angle = angle
            state.steering = steering

            state.wheel_center_x = (
                state.left_hand.wrist_x
                + state.right_hand.wrist_x
            ) / 2.0

            state.wheel_center_y = (
                state.left_hand.wrist_y
                + state.right_hand.wrist_y
            ) / 2.0

            distance = self.pixel_distance(
                (
                    state.left_hand.wrist_x,
                    state.left_hand.wrist_y,
                ),
                (
                    state.right_hand.wrist_x,
                    state.right_hand.wrist_y,
                ),
            )
            state.wheel_radius = (distance * 0.65)

        if state.left_hand is not None:
            state.left_fist = (state.left_hand.is_fist)
            state.left_open = (state.left_hand.is_open)
        if state.right_hand is not None:
            state.right_fist = (state.right_hand.is_fist)
            state.right_open = (state.right_hand.is_open)

        if (state.left_fist and state.right_fist):
            state.gas = 1.0

        elif (state.left_open and state.right_open):
            state.brake = 1.0

        return state