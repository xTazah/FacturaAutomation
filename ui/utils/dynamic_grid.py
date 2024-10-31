import tkinter as tk

class DynamicGrid(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.text = tk.Text(self, wrap="char", borderwidth=0, highlightthickness=0,
                            state="disabled")
        self.text.pack(fill="both", expand=True)
        self.boxes = []

    def add_box(self, image=None):
        box = tk.Canvas(self.text, width=100, height=100, bg="white", bd=1, relief="sunken")
        if image:
            box.create_image(50, 50, image=image)
            box.image = image  # keep image reference to prevent garbage collection
        self.boxes.append(box)
        self.text.configure(state="normal")
        self.text.window_create("end", window=box)
        self.text.configure(state="disabled")
        return box