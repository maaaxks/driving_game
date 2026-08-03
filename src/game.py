from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from src import settings
from src.world import World
from src.car import Car
from src.camera_controller import CameraController
from src.input_manager import InputManager


class DrivingGame(ShowBase):
    def __init__(self):
        super().__init__()
        self._setup_window()
        self.disableMouse()
        self.world = World(self)
        self.car = Car(self)
        self.input = InputManager(self)
        self.camera_controller = CameraController(self, self.car)
        self.taskMgr.add(self.update, "update")

    def _setup_window(self):
        props = WindowProperties()
        props.setTitle(settings.WINDOW_TITLE)
        props.setSize(settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        self.win.requestProperties(props)

    def update(self, task):
        dt = globalClock.getDt()
        self.car.update(dt, self.input)
        self.camera_controller.update(dt)
        return task.cont