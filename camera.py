import cv2

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
            # ToDo: save correctly with metadata that it has not been processed
            cv2.imwrite("screenshot.png", frame)
        else:
            raise EnvironmentError

    def release(self):
        self.cap.release()