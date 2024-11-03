import cv2

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(1)  # basic camera
        self.cap.set( cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set( cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    def get_frame(self):
        ret, frame = self.cap.read()
        if ret:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #cpnvert to rbg
        return None

    def take_photo(self):
        frame = self.get_frame()
        if frame is not None:
            return frame
        else:
            raise EnvironmentError("Cannot capture image")

    def release(self):
        self.cap.release()