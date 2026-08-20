class InputManager:
    def __init__(self, game):

        self.game =game
        self.gas = 0.0
        self.brake = 0.0

        self.target_steering = 0.0

        self.keyboard_gas = 0.0
        self.keyboard_brake = 0.0
        self.keyboard_steering = 0.0

        self.vision_enabled = False

        self.vision_gas = 0.0
        self.vision_brake = 0.0
        self.vision_steering = 0.0

        game.accept("w", self.set_gas, [1.0])
        game.accept("w-up", self.set_gas, [0.0])

        game.accept("s", self.set_brake, [1.0])
        game.accept("s-up", self.set_brake, [0.0])

        game.accept("a", self.set_steering, [-1.0])
        game.accept("a-up", self.set_steering, [0.0])

        game.accept("d", self.set_steering, [1.0])
        game.accept("d-up", self.set_steering, [0.0])

    def set_gas(self, value):
        self.gas = value

    def set_brake(self, value):
        self.brake = value

    def set_steering(self, value):
        self.target_steering = value

    def set_vision_input(self, steering, gas, brake):
        self.vision_steering = steering
        self.vision_gas = gas
        self.vision_brake = brake

    def set_vision_enabled(self, enabled):
        self.vision_enabled = enabled

    def update(self):
        if self.vision_enabled:
            self.target_steering = (self.vision_steering)
            self.gas = (self.vision_gas)
            self.brake = (self.vision_brake)
        else:
            self.target_steering = (self.keyboard_steering)
            self.gas = (self.keyboard_gas)
            self.brake = (self.keyboard_brake)