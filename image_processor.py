import threading
from queue import Queue

# this class handles the processing of the images
class ImageProcessor:
    def __init__(self):
        self.image_queue = Queue()