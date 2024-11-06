import threading
import time
from queue import Queue, Empty
from PIL import Image, PngImagePlugin
import cv2
import numpy as np

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
        img = Image.open(image_path)
        
        # update metadata to indicate processing started
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("status", "Processing")
        img.save(image_path, "PNG", pnginfo=metadata)
        
        print(f"Processing image: {image_path}")

        img_cv = cv2.imread(image_path)

        img = self.preprocess_image(img_cv)
        img.show()

        # update metadata
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("status", "Completed")
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
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

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
            target_height = 1600 
            target_width = int(target_height * 3 / 4)

            # calculate corners for warping
            dst_corners = np.float32([[0, 0], [0, target_height], [target_width, target_height], [target_width, 0]])

            # warps perspective 
            M_warp = cv2.getPerspectiveTransform(dst, dst_corners)
            factura_warped = cv2.warpPerspective(img, M_warp, (target_width, target_height))

            return Image.fromarray(cv2.cvtColor(factura_warped, cv2.COLOR_BGR2RGB))
        else:
            raise Exception("No factura found in the image.")