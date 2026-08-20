from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from src import settings
from src.world import World
from src.car import Car
from src.camera_controller import CameraController
from src.input_manager import InputManager
from src.gesture_reader import GestureReader
from src.vision_display import VisionDisplay


class DrivingGame(ShowBase):
    def __init__(self):
        super().__init__()
        self._setup_window()
        self.disableMouse()
        self.world = World(self)
        self.car = Car(self)
        self.input = InputManager(self)
        self.gesture_reader = GestureReader()
        self.gesture_reader.start()
        self.input.set_vision_enabled(True)
        self.vision_display = VisionDisplay(self, self.gesture_reader)
        self.camera_controller = CameraController(self, self.car)
        self.taskMgr.add(self.update, "update")

    def _setup_window(self):
        props = WindowProperties()
        props.setTitle(settings.WINDOW_TITLE)
        props.setSize(settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        self.win.requestProperties(props)

    def toggle_vision(self):
        enabled = (not self.input.vision_enabled)
        self.input.set_vision_enabled(enabled)

        print(
            "VISION:",
            "ON" if enabled else "OFF"
        )

    def quit_game(self):
        self.gesture_reader.stop()
        self.userExit()

    def update(self, task):
        dt = globalClock.getDt()
        self.gesture_reader.update()

        self.input.set_vision_input(
            steering=(
                self.gesture_reader
                .get_steering()
            ),

            gas=(
                self.gesture_reader
                .get_gas()
            ),

            brake=(
                self.gesture_reader
                .get_brake()
            ),
        )
        self.input.update()
        self.car.update(dt, self.input)
        self.camera_controller.update(dt)
        self.vision_display.update()

        return task.cont