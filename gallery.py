from queue import Queue
import os
import cv2
import json
from PIL import Image, PngImagePlugin

# handles saving images to filesystem, reading all images on startup and handling file metadata
class Gallery:
    def __init__(self, image_queue: Queue) -> None:
        os.makedirs("captured_images",exist_ok= True)

        self.highest_image_number = self.get_highest_image_number() # get inital highest image number

        #ToDo: load images initally and then have watchdog react to changes in the image list and then update the ui

    def get_highest_image_number(self):
        image_files = [f for f in os.listdir("captured_images") if f.startswith("image") and f.endswith(".png")]
        if not image_files:
            return 1

        highest_image_number = max(int(f.split("_")[-2:-1][0]) for f in image_files)

        return highest_image_number + 1

    def save_image(self, image):
        filename = f"captured_images/image_{self.highest_image_number}_.png"
        while os.path.exists(filename):
                self.highest_image_number += 1
                filename = f"captured_images/image_{self.highest_image_number}_.png"
            
        #cv2.imwrite(filename, image) #metadata--> processed: false ; factura_number: 245892 or None
        
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("processed", "False")
        metadata.add_text("number", "0")

        Image.fromarray(image).save(filename, "PNG", pnginfo=metadata)

        # self.create_toast(f"image_{self.highest_image_number}_.png saved", 1500)
    
    def get_images(self):
         images = []
         for filename in os.listdir("captured_images"):
              image_path = os.path.join("captured_images", filename)
              if image_path.endswith(".png"):
                   images.append(Image.open(image_path))

         return images

                   

    def load_image(self, filename):
         
        image = Image.open(filename)
        metadata = image.info
        # print(image.info.get("processed"))
        # print(image.info.get("number"))
        # print(image.info.get("test"))
        # print(type(image.info.get("processed")))
        # print(type(image.info.get("number")))
        # print(type(image.info.get("test")))
        return image, metadata