import tkinter as tk
from PIL import ImageTk, PngImagePlugin
from gallery import Gallery
#  todo

class GalleryScreen(tk.Frame):
    def __init__(self, master, gallery: Gallery):
        super().__init__(master)
        self.images = gallery.get_images() #ToDo should be getting this from a property instead

        width = self.winfo_width()
        print(width)
        columns = max(1,width //120) # set columns count dynmaically # ToDo: should calculate this based on variables (img width, padding, etc.) so if changed everything works as expected
        for idx, img in enumerate(self.images):
            row = idx // columns
            col = idx % columns
            print("row: " , row, "col: " , col)
            tk_img = ImageTk.PhotoImage(img.resize((100,100)))
            # container = tk.Frame(master)
            # container.pack(side="left")
            #label = tk.Label(master, bg ="black", width=15, height=7)
            # label = tk.Label(master, image= tk_img)
            #label.image = tk_img
            #label.grid(row=row, column=col, padx= 5, pady = 5) #ToDo: variables


            canvas = tk.Canvas(self, width=100, height=100, bg="white")
            canvas.create_image(50, 50, image=tk_img)  # Bild in der Mitte des Canvas platzieren
            canvas.image = tk_img  # Bildreferenz halten, damit das Bild nicht gelöscht wird
            canvas.grid(row=row, column=col, padx=5, pady=5)