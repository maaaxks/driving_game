import math
from panda3d.core import Vec3

class CarController:

    def __init__(self, car_node):

        self.car_node = car_node
        self.speed = 0.0
        self.max_speed = 20.0
        self.acceleration = 10.0
        self.brake_strength = 25.0
        self.friction = 4.0
        self.steering = 0.0
        self.steering_sensitivity = 0.65
        self.turn_speed = 100.0
        self.gas = 0.0
        self.brake = 0.0
        self.angle = 0.0

    def set_input(self, steering, gas, brake):

        self.steering = max(-1.0, min(1.0, steering))
        self.gas = max(0.0, min(1.0, gas))
        self.brake = max(0.0, min(1.0, brake))

    def update(self, dt):

        self._update_speed(dt)
        self._update_rotation(dt)
        self._update_position(dt)

    def _update_speed(self, dt):

        if self.gas > 0.0:
            self.speed += (self.acceleration * self.gas * dt)

        if self.brake > 0.0:
            self.speed -= (self.brake_strength * self.brake * dt)

        elif self.gas <= 0.0:
            if self.speed > 0.0:
                self.speed -= (self.friction * dt)

        if self.speed < 0.0:
            self.speed = 0.0
        if self.speed > self.max_speed:
            self.speed = self.max_speed

    def _update_rotation(self, dt):

        if abs(self.speed) < 0.05:
            return

        speed_factor = min(abs(self.speed) / self.max_speed, 1.0)
        steering = (self.steering * self.steering_sensitivity)
        turn_amount = (steering * self.turn_speed * speed_factor * dt)
        self.angle -= turn_amount
        self.car_node.setH(self.angle)

    def _update_position(self, dt):

        angle_rad = math.radians(self.angle)
        dx = (self.speed * dt * math.sin(angle_rad))
        dy = (self.speed * dt * math.cos(angle_rad))
        current_pos = (self.car_node.getPos())
        self.car_node.setPos(current_pos + Vec3(dx, dy, 0))

    def get_speed(self):

        return self.speed

    def get_angle(self):

        return self.angle

    def get_position(self):

        return self.car_node.getPos()