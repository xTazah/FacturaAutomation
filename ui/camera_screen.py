import tkinter as tk
from PIL import Image, ImageTk
from camera import Camera

class CameraScreen(tk.Frame):
    def __init__(self, master, camera: Camera, create_toast):
        super().__init__(master)
        self.create_toast = create_toast
        self.master = master
        self.camera = camera

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
        self.camera.take_photo()
        self.create_toast("Photo taken", 3000)

    def __del__(self):
        self.camera.release()
