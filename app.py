import tkinter as tk
from ui.main_screen import MainScreen
from settings_manager import SettingsManager
from camera import Camera
from gallery import Gallery

class App:
    def __init__(self):
        self.settings_manager = SettingsManager()
        self.camera = Camera()
        self.gallery = Gallery()

        self.root = tk.Tk()
        self.root.resizable(False, False) #ToDo: should be accessible trough settings only
        width = self.settings_manager.get("window_width", 1280)
        height = self.settings_manager.get("window_height", 720)
        self.root.geometry(f"{width}x{height}")
        self.root.update_idletasks() # needs to be called so the geometry actually changes...
        self.root.title("Factura Automation")

        # resize event
        self.root.bind("<Configure>", self.on_resize)

        self.main_screen = MainScreen(self.root, self.settings_manager, self.camera, self.gallery)


    def on_resize(self, event):
        if event.widget == self.root:
            self.settings_manager.set("window_width", self.root.winfo_width())
            self.settings_manager.set("window_height", self.root.winfo_height())

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
