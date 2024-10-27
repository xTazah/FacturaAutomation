import cv2
import os

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)  # basic camera

    def get_frame(self):
        ret, frame = self.cap.read()
        if ret:
            return frame
        return None

    def take_photo(self):
        frame = self.get_frame()
        if frame is not None:
            return frame
        else:
            raise EnvironmentError("Cannot capture image")

    def release(self):
        self.cap.release()