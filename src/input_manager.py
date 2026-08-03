class InputManager:
    def __init__(self, game):

        self.game =game
        self.gas = 0.0
        self.brake = 0.0

        self.target_steering = 0.0

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