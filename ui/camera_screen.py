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

        self.btn_capture = tk.Button(self,text="Take picture", command=self.take_photo)
        padY=10
        self.btn_capture.grid(row=1, column=0, pady=padY)
        self.master.update_idletasks()
        self.canvas = tk.Canvas(self, width=self.master.winfo_width(), height=self.master.winfo_height() - self.btn_capture.winfo_height()-padY*2)
        self.canvas.grid(row=0, column=0)

        self.update_camera()

    def update_camera(self):
        frame = self.camera.get_frame()
        if frame is not None:
            img = Image.fromarray(frame).resize([self.canvas.winfo_width(), self.canvas.winfo_height()] )
            imgtk = ImageTk.PhotoImage(image=img)
            
            self.canvas.create_image(0, 0, image=imgtk, anchor="nw")
            self.canvas.imgtk = imgtk 
        self.after(25, self.update_camera)  # call again after 25 ms --> 40fps

    def take_photo(self):
        image = self.camera.take_photo()
        self.gallery.save_image(image)

    def __del__(self):
        self.camera.release()
