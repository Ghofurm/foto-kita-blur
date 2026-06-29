import cv2

class Camera:
    def __init__(self, device_id=0, width=640, height=480):
        self.device_id = device_id
        self.width = width
        self.height = height
        self.cap = None

    def start(self):
        self.cap = cv2.VideoCapture(self.device_id)
        if not self.cap.isOpened():
            raise RuntimeError(f"Tidak dapat membuka kamera dengan ID {self.device_id}")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def read(self):
        if self.cap is None or not self.cap.isOpened():
            return False, None
        return self.cap.read()

    def release(self):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
            self.cap = None

