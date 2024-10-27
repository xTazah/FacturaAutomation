import tkinter as tk
from PIL import Image, ImageTk
import cv2

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)  # 0 für die Standardkamera

    def get_frame(self):
        ret, frame = self.cap.read()
        if ret:
            return frame
        return None

    def take_photo(self):
        frame = self.get_frame()
        if frame is not None:
            # Hier könntest du den Screenshot speichern
            cv2.imwrite("screenshot.png", frame)

    def release(self):
        self.cap.release()  # Kamera freigeben


class CameraScreen(tk.Frame):
    def __init__(self, master, on_settings):
        super().__init__(master)
        self.on_settings = on_settings

        # Kamera-Objekt erstellen
        self.camera = Camera()

        self.canvas = tk.Canvas(self, width=640, height=480)
        self.canvas.grid(row=0, column=0)

        self.btn_capture = tk.Button(self, text="Foto machen", command=self.take_photo)
        self.btn_capture.grid(row=1, column=0, pady=10)

        self.update_camera()

    def update_camera(self):
        frame = self.camera.get_frame()
        if frame is not None:
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, image=imgtk, anchor="nw")
            self.canvas.imgtk = imgtk  # Referenz halten
        self.after(10, self.update_camera)  # Wiederhole alle 10 ms

    def take_photo(self):
        self.camera.take_photo()  # Nimmt ein Bild auf

    def __del__(self):
        self.camera.release()  # Kamera freigeben
