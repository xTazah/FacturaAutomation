import tkinter as tk
import os, subprocess

class DynamicGrid(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # frame that holds boxes and scrollbar
        self.scrollable_frame = tk.Frame(self)
        self.scrollable_frame.pack(fill="both", expand=True)

        # vrtical scrollbar
        self.scrollbar = tk.Scrollbar(self.scrollable_frame, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.text = tk.Text(self.scrollable_frame, wrap="char", borderwidth=0, highlightthickness=0,
                            state="disabled", yscrollcommand=self.scrollbar.set)
        self.text.pack(fill="both", expand=True)

        # configure to scroll the text widget
        self.scrollbar.config(command=self.text.yview)

        self.boxes = []

    def add_box(self, image, image_path= None):
        box = tk.Canvas(self.text, width=100, height=100, bg="white", bd=1, relief="sunken")
        if image:
            box.create_image(50, 50, image=image)
            box.image = image  # keep image reference to prevent garbage collection

        if image_path:
            box.bind("<Button-1>", lambda event: self.open_image(image_path))

        self.boxes.append(box)
        self.text.configure(state="normal")
        self.text.window_create("end", window=box)
        self.text.configure(state="disabled")
        return box
    
    #ToDo: get absolute filepath from gallery.py and then use it in add_box
    def open_image(self, image_path):
        # ToDo: popup to make it big and do a rerun manually
        pass