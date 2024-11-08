import tkinter as tk
from PIL import Image, ImageTk
from model.camera import Camera
from model.gallery import Gallery

class CameraScreen(tk.Frame):
    def __init__(self, master, camera: Camera, gallery: Gallery):
        super().__init__(master)
        self.master = master
        self.camera = camera
        self.gallery = gallery

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.btn_capture = tk.Button(self, text="Take picture", command=self.take_photo)
        self.btn_capture.grid(row=1, column=0, pady=10)

        # canvas that fills entire space
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0, column=0, sticky='nsew')

        #start update lopo
        self.update_camera()

    def update_camera(self):
        frame = self.camera.get_frame()
        if frame is not None:
            img = Image.fromarray(frame)
            img, canvas_width, canvas_height = self.resize_image(img)
            self.tk_image = ImageTk.PhotoImage(img) #hold reference to prevent garbage collection
            self.canvas.delete("all")
            self.canvas.create_image(canvas_width // 2, canvas_height // 2, image=self.tk_image)
        self.after(25, self.update_camera)  # call again after 25 ms --> 40fps

    #resize image to fit canvas and retain aspect ratio
    def resize_image(self, img):
        canvas_width, canvas_height = self.canvas.winfo_width(), self.canvas.winfo_height()
        aspect_ratio = 16 / 9

        if canvas_width <= 0 or canvas_height <= 0:
            return img, canvas_width, canvas_height  # Return original image if canvas dimensions are invalid

        if (canvas_width / canvas_height) > aspect_ratio:
            new_height = canvas_height
            new_width = int(new_height * aspect_ratio)
        else:
            new_width = canvas_width
            new_height = int(new_width / aspect_ratio)

        new_width = max(1, new_width)  # Ensure new width is at least 1
        new_height = max(1, new_height)  # Ensure new height is at least 1

        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        return img, canvas_width, canvas_height


    def take_photo(self):
        image = self.camera.take_photo()
        self.gallery.save_image(image)

    def __del__(self):
        self.camera.release()
