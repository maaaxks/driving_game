import math
import cv2
from panda3d.core import (Texture, CardMaker, Camera, OrthographicLens)
from src import settings


class VisionDisplay:

    def __init__(self, game, gesture_reader):
        self.game = game
        self.gesture_reader = gesture_reader

        self.texture = Texture("vision_texture")
        self.card = None
        self._create_display()

    def set_display_region(self, display_region):
        self.display_region = display_region
        self.display_region.setCamera(self.camera_np)

    def _create_display(self):
        card_maker = CardMaker("vision_card")

        aspect = settings.GAME_SCREEN_RATIO
        card_maker.setFrame(
            -1,
            1,
            -1.0,
            1.0
        )

        self.card = (
            self.game.render2d.attachNewNode(
                card_maker.generate()
            )
        )

        self.card.setTexture(self.texture)


    def _draw_hand_landmarks(self, frame, hand):

        landmarks = hand.landmarks

        height, width = frame.shape[:2]

        connections = [

            #Thumb
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4),

            #Index
            (0, 5),
            (5, 6),
            (6, 7),
            (7, 8),

            #Middle
            (0, 9),
            (9, 10),
            (10, 11),
            (11, 12),

            #ring
            (0, 13),
            (13, 14),
            (14, 15),
            (15, 16),

            #Pinky
            (0, 17),
            (17, 18),
            (18, 19),
            (19, 20),

            #Palm
            (5, 9),
            (9, 13),
            (13, 17),
        ]

        for start, end in connections:
            x1 = int(landmarks[start].x * width)

            y1 = int(landmarks[start].y * height)

            x2 = int(landmarks[end].x * width)

            y2 = int(landmarks[end].y * height)

            cv2.line(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2,
            )
        for index, landmark in enumerate(landmarks):

            x = int(landmark.x * width)

            y = int(landmark.y * height)

            cv2.circle(
                frame,
                (x, y),
                5,
                (0, 0, 255),
                -1,
            )

            cv2.putText(
                frame,
                str(index),
                (x + 5, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.35,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )

        cv2.putText(
            frame,
            hand.handedness,
            (
                int(hand.wrist_x),
                int(hand.wrist_y) - 20,
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2,
            cv2.LINE_AA,
        )

    def _draw_virtual_wheel(self, frame, state):

        if not state.hands_visible:
            return

        if (
            state.left_hand is None
            or state.right_hand is None
        ):
            return

        center = (int(state.wheel_center_x), int(state.wheel_center_y))
        radius = int(state.wheel_radius)

        if radius < 20:
            return

        cv2.circle(
            frame,
            center,
            radius,
            (255, 180, 0),
            3,
        )

        cv2.circle(
            frame,
            center,
            max(
                5,
                int(radius * 0.12)
            ),
            (255, 180, 0),
            2,
        )
        angle = math.radians(-state.steering_angle)
        end_x = int(center[0] + math.cos(angle) * radius)
        end_y = int(center[1] - math.sin(angle) * radius)

        cv2.line(
            frame,
            center,
            (end_x, end_y),
            (0, 200, 255),
            4,
        )

    def _draw_info(self, frame, state, fps):
        lines = [

            f"FPS: {fps:.1f}",

            (
                "Hands: "
                f"{int(state.left_hand is not None) + int(state.right_hand is not None)}"
            ),

            (
                "Steering angle: "
                f"{state.steering_angle:+.1f} deg"
            ),

            (
                "Steering: "
                f"{state.steering:+.2f}"
            ),

            (
                "Gas: "
                f"{state.gas:.1f}"
            ),

            (
                "Brake: "
                f"{state.brake:.1f}"
            ),

            (
                "Left fist: "
                f"{state.left_fist}"
            ),

            (
                "Right fist: "
                f"{state.right_fist}"
            ),

            (
                "Left open: "
                f"{state.left_open}"
            ),

            (
                "Right open: "
                f"{state.right_open}"
            ),
        ]
        x = 15
        y = 25

        for line in lines:
            cv2.putText(
                frame,
                line,
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )

            y += 25

    def _prepare_frame_for_display(self, frame):
        target_ratio = (settings.GAME_SCREEN_RATIO)

        height, width = frame.shape[:2]
        current_ratio = width / height

        if current_ratio > target_ratio:
            new_width = int(height * target_ratio)
            left = (width - new_width) // 2

            frame = frame[:, left:left + new_width]

        elif current_ratio < target_ratio:
            new_height = int( width / target_ratio)
            top = ( height - new_height ) // 2

            frame = frame[top:top + new_height, :]

        return frame

    def update(self):
        frame = (self.gesture_reader.get_frame())
        state = (self.gesture_reader.get_state())
        if frame is None or state is None:
            return

        frame = frame.copy()
        if state.left_hand is not None:
            self._draw_hand_landmarks(frame, state.left_hand)

        if state.right_hand is not None:
            self._draw_hand_landmarks(frame, state.right_hand)

        self._draw_virtual_wheel(frame, state)
        self._draw_info(frame, state, self.gesture_reader.vision.fps)
        frame=(self._prepare_frame_for_display(frame))
        frame = cv2.flip(frame, 0)
        height, width = frame.shape[:2]
        self.texture.setup2dTexture(
            width,
            height,
            Texture.T_unsigned_byte,
            Texture.F_rgb,
        )
        self.texture.setRamImage(frame.tobytes())