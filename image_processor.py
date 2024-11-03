import threading
import time
from queue import Queue, Empty
from PIL import Image, PngImagePlugin
import cv2

class ImageProcessorThread(threading.Thread):
    def __init__(self, image_queue: Queue, shutdown_event):
        super().__init__(daemon=True)  # terminate with main program
        self.image_queue = image_queue
        self.shutdown_event = shutdown_event

    def run(self):
        retry = 0
        while not self.shutdown_event.is_set():
            try:
                # get next image, if empty after retry (max 10) sec throws exception and check for shutdown (equal to time.sleep(retry))
                image_path = self.image_queue.get(timeout= retry)

                self.process_image(image_path)

                # mark the task as done (idk why but this is important?)
                self.image_queue.task_done()

                retry = 0
            except Empty:
                retry = min(retry + 1, 10) #increase wait time
                print(f"Queue empty. Waiting {retry} second{'s' if retry != 1 else ''}")
                continue

    def process_image(self, image_path):
        img = Image.open(image_path)
        
        # update metadata to indicate processing started
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("status", "Processing")
        img.save(image_path, "PNG", pnginfo=metadata)
        
        print(f"Processing image: {image_path}")




        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Use Canny edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Assume the largest contour is the factura
        factura_contour = max(contours, key=cv2.contourArea)
        
        # Get the bounding box of the factura
        x, y, w, h = cv2.boundingRect(factura_contour)
        
        # Crop the image to the bounding box
        factura = img[y:y+h, x:x+w]
        
        # Save or return the cropped image
        cv2.imwrite("cropped_factura.jpg", factura)






        # update metadata
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("status", "Completed")
        img.save(image_path, "PNG", pnginfo=metadata)

        print(f"Processed image: {image_path}")
