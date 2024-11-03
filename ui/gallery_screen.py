import tkinter as tk
from PIL import ImageTk, PngImagePlugin
from gallery import Gallery
from ui.utils.dynamic_grid import DynamicGrid
#  todo
class GalleryScreen(tk.Frame):
    def __init__(self, master: tk.Tk, gallery:Gallery):
        super().__init__(master)
        self.gallery = gallery
        self.grid(row=0, column=0, sticky="nsew")
        
        # Make sure GalleryScreen expands to fill available space
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.master.update_idletasks()

        # Create and add DynamicGrid
        self.dynamic_grid = DynamicGrid(self)
        self.dynamic_grid.grid(row=0, column=0, sticky="nsew")
        self.dynamic_grid.update_idletasks()
        
        # subscribe to gallery update events
        self.gallery.event_dispatcher.subscribe("gallery_image_added", self.gallery_image_added_callback)
        self.gallery.event_dispatcher.subscribe("gallery_image_deleted", self.gallery_image_deleted_callback)

        # dict to map boxes to filepaths
        self.box_dict = {} 

        self.render_gallery()

    def render_gallery(self):
        """inital rendering of all images """
        for filename, img in self.gallery.images.items():
            self.add_image(filename, img)

    def add_image(self, filename, img):
        """adds a new image to the grid"""
        tk_img = ImageTk.PhotoImage(img.resize((100, 100)))
        box = self.dynamic_grid.add_box(image=tk_img)
        box.image = tk_img  # Keep reference to avoid garbage collection
        self.box_dict[filename] = box  # Track box by filename

    def remove_image(self, filename):
        """removes a specific image box from the grid"""
        box = self.box_dict.pop(filename)
        if box:
            print("box found")
            box.destroy()

    ######################## Callbacks ########################
    
    def gallery_image_added_callback(self, args):
        self.add_image(args[0],args[1])
    
    def gallery_image_deleted_callback(self, args):
        self.remove_image(args[0])