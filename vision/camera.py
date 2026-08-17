import cv2

class Camera:
    def __init__(self, camera_index=0, width=640, height=480):
        self.camera_index=camera_index
        self.width=width
        self.height=height
        self.capture=None

    def open(self):
        self.capture=cv2.VideoCapture(self.camera_index)
        if not self.capture.isOpened():
            raise RuntimeError(f"Camera cannot open")
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def read(self):
        success, frame=self.capture.read()
        if not success:
            return None
        frame=cv2.flip(frame, 1)

        return frame
    def release(self):
        if self.capture is not None:
            self.capture.release()
            self.capture=None
