from queue import Queue
import os
import cv2
import json
from PIL import Image, PngImagePlugin
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from event_dispatcher import EventDispatcher

# handles saving images to filesystem, reading all images on startup and handling file metadata
class Gallery:
    def __init__(self, image_queue: Queue):
        os.makedirs("captured_images", exist_ok=True)
        self.highest_image_number = self.get_highest_image_number()
        self.image_queue = image_queue
        self.images = {}
        self.event_dispatcher = EventDispatcher()  # Event Dispatcher für Event-Abos
        self.load_images()

        # Setup Watchdog
        self.event_handler = GalleryEventHandler(self.on_image_folder_change)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, "captured_images", recursive=False)
        self.observer.start()

    def get_highest_image_number(self):
        image_files = [f for f in os.listdir("captured_images") if f.startswith("image") and f.endswith(".png")]
        return max((int(f.split("_")[-2]) for f in image_files), default=0) + 1

    def save_image(self, image):
        filename = f"captured_images/image_{self.highest_image_number}_.png"
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("processed", "False")
        Image.fromarray(image).save(filename, "PNG", pnginfo=metadata)
        self.highest_image_number += 1

    def load_images(self):
        for filename in os.listdir("captured_images"):
            image_path = os.path.join("captured_images", filename)
            self.load_image(image_path)

    def on_image_folder_change(self, event):
        # Refresh images based on file system event
        if event.event_type == "created":
            time.sleep(0.2) # wait for file-handle to close (watchdog calls event before the file is created fully)
            self.event_dispatcher.publish("gallery_image_added", [event.src_path, self.load_image(event.src_path)])

        elif event.event_type == "deleted":
            self.event_dispatcher.publish("gallery_image_deleted", [event.src_path])

        elif event.event_type == "modified":
            pass #toDo
        else:
            pass #ToDo error handling
    
    def load_image(self, image_path):
        if image_path.endswith(".png"):
            try:
                with Image.open(image_path) as img: # ensure file handle is closed 
                        self.images[image_path] = img.copy()  # make a copy in memory
            except PngImagePlugin.UnidentifiedImageError:
                print(f"Warning: Could not identify image file {image_path}")
                return None
        
           # metadata = image.info
            
            # print(image.info.get("processed"))
            # print(image.info.get("number"))
            # print(image.info.get("test"))
            # print(type(image.info.get("processed")))
            # print(type(image.info.get("number")))
            # print(type(image.info.get("test")))
            # return image, metadata


            return self.images[image_path]
        else:
            return None

class GalleryEventHandler(FileSystemEventHandler):
     def __init__(self, callback):
         super().__init__()
         self.callback = callback

     def on_created(self, event):
         if not event.is_directory:
             self.callback(event)

     def on_modified(self, event):
         if not event.is_directory:
             self.callback(event)

     def on_deleted(self, event):
         if not event.is_directory:
             self.callback(event)
