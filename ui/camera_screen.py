import tkinter as tk
from PIL import Image, ImageTk
from camera import Camera
from gallery import Gallery

class CameraScreen(tk.Frame):
    def __init__(self, master, camera: Camera, gallery: Gallery):
        super().__init__(master)
        self.master = master
        self.camera = camera
        self.gallery = gallery

        self.canvas = tk.Canvas(self, width=640, height=480)
        self.canvas.grid(row=0, column=0)

        self.btn_capture = tk.Button(self, text="Take picture", command=self.take_photo)
        self.btn_capture.grid(row=1, column=0, pady=10)

        self.update_camera()

    def update_camera(self):
        frame = self.camera.get_frame()
        if frame is not None:
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            
            self.canvas.create_image(0, 0, image=imgtk, anchor="nw")
            self.canvas.imgtk = imgtk 
        self.after(10, self.update_camera)  # call again after 10 ms

    def take_photo(self):
        image = self.camera.take_photo()
        self.gallery.save_image(image)

    def __del__(self):
        self.camera.release()
