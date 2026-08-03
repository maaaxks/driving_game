from panda3d.core import Vec3
from src import settings

class Car:
    def __init__(self, game):

        self.game = game
        #scene graph
        self.node = game.render.attachNewNode("Car")

        self.model = game.loader.loadModel("models/car/car.gltf")
        self.model.reparentTo(self.node)

        self.model.setScale(settings.CAR_SCALE)
        self.model.setZ(0.5)
        self.model.setH(90)

        self.camera_mount = self.node.attachNewNode("CameraMount")
        self.camera_mount.setPos(settings.CAMERA_OFFSET)

        #physics
        self.speed = 0.0
        self.steering = 0.0
        self.position = Vec3(0, 0, 0)

    def update(self, dt, input_manager):
        if input_manager.gas > 0:
            self.speed += (
                settings.ACCELERATION
                * input_manager.gas
                * dt
            )
        if input_manager.brake > 0:
            self.speed -= (
                settings.BRAKE_FORCE
                * input_manager.brake
                * dt
            )
        if input_manager.gas == 0:
            self.speed -= settings.DRAG * dt
        self.speed = max(0.0, self.speed)
        self.speed = min(settings.MAX_SPEED, self.speed)
        self.steering += (
            input_manager.target_steering

            - self.steering

        ) * settings.STEERING_SMOOTHNESS * dt
        if self.speed > 0.1:

            turn = (
                self.steering

                * settings.MAX_TURN_RATE

                * (self.speed / settings.MAX_SPEED)

                * dt
            )
            self.node.setH(self.node.getH() -turn)
        self.node.setY(self.node, self.speed * dt)