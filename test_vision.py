import cv2

from vision.vision_manager import VisionManager


def draw_hand_landmarks(
    frame,
    hand,
):

    landmarks = hand.landmarks

    height, width = frame.shape[:2]

    # Соединения между landmark'ами.
    connections = [

        # Большой палец
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),

        # Указательный
        (0, 5),
        (5, 6),
        (6, 7),
        (7, 8),

        # Средний
        (0, 9),
        (9, 10),
        (10, 11),
        (11, 12),

        # Безымянный
        (0, 13),
        (13, 14),
        (14, 15),
        (15, 16),

        # Мизинец
        (0, 17),
        (17, 18),
        (18, 19),
        (19, 20),

        # Ладонь
        (5, 9),
        (9, 13),
        (13, 17),
    ]

    for start, end in connections:

        x1 = int(
            landmarks[start].x * width
        )

        y1 = int(
            landmarks[start].y * height
        )

        x2 = int(
            landmarks[end].x * width
        )

        y2 = int(
            landmarks[end].y * height
        )

        cv2.line(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2,
        )

    for index, landmark in enumerate(
        landmarks
    ):

        x = int(
            landmark.x * width
        )

        y = int(
            landmark.y * height
        )

        cv2.circle(
            frame,
            (x, y),
            5,
            (0, 0, 255),
            -1,
        )

        # Номер точки.
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

    # Подпись руки.
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


def draw_virtual_wheel(
    frame,
    state,
):

    if not state.hands_visible:

        return

    # Руль рисуем только если есть две руки.
    if (
        state.left_hand is None
        or state.right_hand is None
    ):

        return

    center = (
        int(state.wheel_center_x),
        int(state.wheel_center_y),
    )

    radius = int(
        state.wheel_radius
    )

    if radius < 20:

        return

    # Основная окружность.
    cv2.circle(
        frame,
        center,
        radius,
        (255, 180, 0),
        3,
    )

    # Внутренняя окружность.
    cv2.circle(
        frame,
        center,
        max(5, int(radius * 0.12)),
        (255, 180, 0),
        2,
    )

    # Линия направления руля.
    #
    # Поворачиваем указатель вместе с углом.
    import math

    angle = math.radians(
        -state.steering_angle
    )

    end_x = int(
        center[0]
        + math.cos(angle) * radius
    )

    end_y = int(
        center[1]
        - math.sin(angle) * radius
    )

    cv2.line(
        frame,
        center,
        (end_x, end_y),
        (0, 200, 255),
        4,
    )


def draw_info(
    frame,
    state,
    fps,
):

    lines = [

        f"FPS: {fps:.1f}",

        f"Hands: "
        f"{int(state.left_hand is not None) + int(state.right_hand is not None)}",

        f"Steering angle: "
        f"{state.steering_angle:+.1f} deg",

        f"Steering: "
        f"{state.steering:+.2f}",

        f"Gas: "
        f"{state.gas:.1f}",

        f"Brake: "
        f"{state.brake:.1f}",

        f"Left fist: "
        f"{state.left_fist}",

        f"Right fist: "
        f"{state.right_fist}",

        f"Left open: "
        f"{state.left_open}",

        f"Right open: "
        f"{state.right_open}",
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

    # Подсказка.
    cv2.putText(
        frame,
        "Q / ESC - exit",
        (
            15,
            frame.shape[0] - 15,
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (200, 200, 200),
        1,
        cv2.LINE_AA,
    )


def main():

    vision = VisionManager(
        model_path="models/vision/hand_landmarker.task",
        camera_index=0,
        camera_width=640,
        camera_height=480,
    )

    try:

        vision.start()

        print("=" * 60)
        print("VISION TEST")
        print("=" * 60)
        print("Камера запущена.")
        print()
        print("Покажи обе руки.")
        print()
        print("Пока что:")
        print("  две руки -> виртуальный руль")
        print("  два кулака -> GAS")
        print("  две открытые ладони -> BRAKE")
        print()
        print("Q / ESC -> выход")
        print("=" * 60)

        while True:

            frame, state = vision.update()

            if frame is None:

                print(
                    "Не удалось получить кадр "
                    "с камеры."
                )

                break

            # Рисуем landmarks.
            if state.left_hand is not None:

                draw_hand_landmarks(
                    frame,
                    state.left_hand,
                )

            if state.right_hand is not None:

                draw_hand_landmarks(
                    frame,
                    state.right_hand,
                )

            # Рисуем виртуальный руль.
            draw_virtual_wheel(
                frame,
                state,
            )

            # Информация.
            draw_info(
                frame,
                state,
                vision.fps,
            )

            cv2.imshow(
                "Vision Test",
                frame,
            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

            if key == 27:
                break

    except KeyboardInterrupt:

        print("\nStoppin...")

    finally:

        vision.stop()

        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()