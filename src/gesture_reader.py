from vision.vision_manager import VisionManager

class GestureReader:

    def __init__(self):
        self.vision = VisionManager()
        self.frame = None
        self.state = None
        self.running = False

    def start(self):
        self.vision.start()
        self.running = True

    def update(self):
        if not self.running:
            return None
        result = self.vision.update()
        if result is None:
            return None
        frame, state = result
        self.frame = frame
        self.state = state

        return frame

    def get_steering(self):
        if self.state is None:
            return 0.0

        return self.state.steering

    def get_gas(self):
        if self.state is None:
            return 0.0

        return self.state.gas

    def get_brake(self):
        if self.state is None:
            return 0.0

        return self.state.brake

    def get_frame(self):
        return self.frame

    def get_state(self):
        return self.state

    def stop(self):
        if self.running:
            self.vision.stop()
            self.running = False