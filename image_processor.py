import base64
from io import BytesIO
import json
import threading
import openai
import os
import dotenv
from queue import Queue, Empty
from PIL import Image, PngImagePlugin
import cv2
import numpy as np
from pydantic import ValidationError
from ai.response_format import Factura
from exceptions import NoFacturaFoundException

dotenv.load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = openai_api_key

class ImageProcessorThread(threading.Thread):
    def __init__(self, image_queue: Queue, shutdown_event):
        super().__init__(daemon=True)  # terminate with main program

        self.image_queue = image_queue
        self.shutdown_event = shutdown_event

        # sift detector for 
        self.sift = cv2.SIFT_create()
        # FLANN-based matcher
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50) #ToDo check if other number of checks is better (performance and accuracy)

        self.flann = cv2.FlannBasedMatcher(index_params, search_params)

        self.template_img =  cv2.cvtColor(cv2.imread('test/blank_factura.png'), cv2.COLOR_BGR2GRAY)
        self.template_keypoints, self.template_descriptors = self.sift.detectAndCompute(self.template_img, None)

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
                #print(f"Queue empty. Waiting {retry} second{'s' if retry != 1 else ''}")
                continue

    def process_image(self, image_path):
        img = Image.open(image_path).copy()
        
        # update metadata to indicate processing started
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("status", "Processing")
        img.save(image_path, "PNG", pnginfo=metadata)
        
        try:
            img = self.preprocess_image(img)

            factura:Factura = self.send_to_openai(img)

            #ToDo: write to google sheets api

            # update metadata
            metadata.add_text("status", "Completed")
            metadata.add_text("factura", factura.InvoiceNumber)
            img.save(image_path, "PNG", pnginfo=metadata)

        except NoFacturaFoundException:
            metadata.add_text("factura", "False")
            metadata.add_text("status", "Completed")
            img.save(image_path, "PNG", pnginfo=metadata)

        except Exception as e:
            print(e)
            metadata.add_text("status", "Error")
            img.save(image_path, "PNG", pnginfo=metadata)

        print(f"Processed image: {image_path}")

    def preprocess_image(self, img, threshold:float = 0.7):
        """
        Method locates a factura inside the passed image and returns it cropped, scaled, and transformed to 3:4 aspect ratio
        Throws an exception if no factura is found.
        
        Parameters:
            img (PIL.Image.Image): The image to process.
            threshold (float): The threshold for feature matching.

        Returns:
            PIL.Image.Image: The processed factura image.
        """
        print("Preprocessing")
        
        # conver to grayscale for beter matching
        img_gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)

        # detect keypoints and descriptors for image
        img_keypoints, image_descriptors = self.sift.detectAndCompute(img_gray, None)

        matches = self.flann.knnMatch(image_descriptors, self.template_descriptors, k=2)

        # filter good matchse ("lowe's ratio test")
        good_matches = []
        for m, n in matches:
            if m.distance < threshold * n.distance:
                good_matches.append(m)

        # different similar parts (or regions of the picture) are "matches" --> https://docs.opencv.org/3.4/d1/de0/tutorial_py_feature_homography.html
        MIN_MATCH_COUNT = 10
        if len(good_matches) > MIN_MATCH_COUNT:
            # get source and destintion points from matches
            src_pts = np.float32([self.template_keypoints[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([img_keypoints[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)

            # calculates homography
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

            h, w = self.template_img.shape

            # points for the template's corners and map them with homography
            pts = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)

            #always return in 3/4 format
            target_height = 600
            target_width = int(target_height * 3 / 4)

            # calculate corners for warping
            dst_corners = np.float32([[0, 0], [0, target_height], [target_width, target_height], [target_width, 0]])

            # warps perspective 
            M_warp = cv2.getPerspectiveTransform(dst, dst_corners)
            factura_warped = cv2.warpPerspective(np.array(img), M_warp, (target_width, target_height))

            #crop out everything thats not needed to reduce img size (vision tokens are expensive openai angrE)
            factura_cropped = factura_warped[125:target_height - 175, 0:target_width]

            return Image.fromarray(factura_cropped)
        else:
            raise NoFacturaFoundException("No factura found in the image.")
        
    def encode_image(self,img):
        # saves to buffer and then encodes to base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def send_to_openai(self,cropped_image):
        base64_image = self.encode_image(cropped_image)
        with open('./ai/system_prompt.txt', 'r') as file:
            system_prompt = file.read()

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt 
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.63,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format= {
                'type': 'json_schema',
                'json_schema': 
                {
                    "name":"factura", 
                    "schema": Factura.model_json_schema()
                }
            }  
        )
        print(response)

        content_json_str = response["choices"][0]["message"]["content"]

        content_dict = json.loads(content_json_str)

        try:
            factura = Factura(**content_dict)
            print(factura)
        except ValidationError as e:
            print("Error casting to Factura:", e)

        return factura