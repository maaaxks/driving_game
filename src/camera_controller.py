from panda3d.core import Vec3
from src import settings

class CameraController:
    def __init__(self, game, car):
        self.game = game
        self.car = car

    def update(self, dt):
        desired = self.car.camera_mount.getPos(self.game.render)

        current = self.game.camera.getPos()
        current += (desired - current) * settings.CAMERA_SMOOTHNESS * dt
        self.game.camera.setPos(current)

        self.game.camera.lookAt(
            self.car.node.getX(),
            self.car.node.getY(),
            self.car.node.getZ()
            + settings.CAMERA_LOOK_AT_HEIGHT
        )