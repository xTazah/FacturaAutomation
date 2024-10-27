from queue import Queue
import os
import cv2

# handles saving images to filesystem, reading all images on startup and handling file metadata
class Gallery:
    def __init__(self, image_queue: Queue) -> None:
        os.makedirs("captured_images",exist_ok= True)

        self.highest_image_number = self.get_highest_image_number() # get inital highest image number

    def get_highest_image_number(self):
        image_files = [f for f in os.listdir("captured_images") if f.startswith("image") and f.endswith(".png")]
        if not image_files:
            return 1

        highest_image_number = max(int(f.split("_")[-2:-1][0]) for f in image_files)

        return highest_image_number + 1

    def save_image(self, image):
        while os.path.exists(f"captured_images/image_{self.highest_image_number}_.png"):
                self.highest_image_number += 1
            
        cv2.imwrite(f"captured_images/image_{self.highest_image_number}_.png", image) #metadata--> processed: false ; factura_number: 245892 or None
        # self.create_toast(f"image_{self.highest_image_number}_.png saved", 1500)