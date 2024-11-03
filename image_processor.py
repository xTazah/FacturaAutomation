import threading
import time
from queue import Queue, Empty
from PIL import Image, PngImagePlugin

class ImageProcessorThread(threading.Thread):
    def __init__(self, image_queue: Queue, shutdown_event):
        super().__init__(daemon=True)  # terminate with main program
        self.image_queue = image_queue
        self.shutdown_event = shutdown_event

    def run(self):
        while not self.shutdown_event.is_set():
            try:
                # get next image, if empty after 1 sec throws exception and check for shutdown (equal to time.sleep(1))
                image_path = self.image_queue.get(timeout= 1)

                self.process_image(image_path)

                # mark the task as done (idk why but this is important?)
                self.image_queue.task_done()
            except Empty:
                print("Queue empty")
                continue

    def process_image(self, image_path):
        img = Image.open(image_path)
        
        # update metadata to indicate processing started
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("status", "Processing")
        img.save(image_path, "PNG", pnginfo=metadata)
        
        print(f"Processing image: {image_path}")

        time.sleep(2)  # todo: replace with actual processing 

        # update metadata
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("status", "Completed")
        img.save(image_path, "PNG", pnginfo=metadata)

        print(f"Processed image: {image_path}")
