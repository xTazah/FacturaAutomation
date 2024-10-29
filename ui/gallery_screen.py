import tkinter as tk
from PIL import ImageTk, PngImagePlugin
from gallery import Gallery
#  todo

class GalleryScreen(tk.Frame):
    def __init__(self, master, gallery: Gallery):
        super().__init__(master)
        self.images = gallery.get_images() #ToDo should be getting this from a property instead

        print(self.images)
        width = master.winfo_width()
        columns = max(1,width //120) # set columns count dynmaically
        for idx, img in enumerate(self.images):
            print(img)
            row = idx // columns
            col = idx % columns
            tk_img = ImageTk.PhotoImage(img.resize((100,100)))
            # container = tk.Frame(master)
            # container.pack(side="left")
            label = tk.Label(master, image= tk_img)
            #label.image = tk_img
            label.grid(row=row, column=col, padx= 5, pady = 5)