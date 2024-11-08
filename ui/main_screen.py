import tkinter as tk
from tkinter import PhotoImage
from ui.camera_screen import CameraScreen
from ui.settings_screen import SettingsScreen
from ui.gallery_screen import GalleryScreen
from ui.utils.toast import Toast
from ui.utils.button_factory import ButtonFactory
from model.settings_manager import SettingsManager
from model.camera import Camera
import tkinter as tk
from model.gallery import Gallery

class MainScreen:
    def __init__(self, root: tk.Tk, settings_manager: SettingsManager, camera: Camera, gallery: Gallery):
        self.root = root
        self.root.title("Factura Automation")
        self.settings_manager = settings_manager
        self.camera = camera
        self.gallery = gallery

        self.gallery_screen = None
        self.camera_screen = None
        self.settings_screen = None

        self.create_navigation()

        # container that holds the different screens
        self.container = tk.Frame(root)
        self.container.pack(fill=tk.BOTH, expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.root.update_idletasks()

        # show camera screen at startup
        self.current_screen = None
        self.show_screen("camera")

    def create_navigation(self):
        self.nav_frame = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=10)
        self.nav_frame.pack(side=tk.TOP, fill=tk.X)

        self.camera_icon = PhotoImage(file="ui/icons/camera.png")
        self.settings_icon = PhotoImage(file="ui/icons/settings.png")
        self.gallery_icon = PhotoImage(file="ui/icons/gallery.png")

        # Creating the buttons with grid layout to simulate space-between
        ButtonFactory.create_button(self.nav_frame, icon=self.gallery_icon, onClickHandler=lambda: self.show_screen("gallery"), column=0, row=0)
        ButtonFactory.create_button(self.nav_frame, icon=self.camera_icon, onClickHandler=lambda: self.show_screen("camera"), column=1, row=0)
        ButtonFactory.create_button(self.nav_frame, icon=self.settings_icon, onClickHandler=lambda: self.show_screen("settings"), column=2, row=0)


        # Adjusting column weights to achieve space-between effect
        self.nav_frame.grid_columnconfigure(0, weight=1)
        self.nav_frame.grid_columnconfigure(1, weight=1)
        self.nav_frame.grid_columnconfigure(2, weight=1)

    def show_screen(self, screen_type):
        # determine the screen to show
        if screen_type == "camera":
            if not self.camera_screen:
                self.camera_screen = CameraScreen(self.container, self.camera, self.gallery)
            screen = self.camera_screen
        elif screen_type == "settings":
            if not self.settings_screen:
                self.settings_screen = SettingsScreen(self.container, self.settings_manager, self.create_toast)
            screen = self.settings_screen
        elif screen_type == "gallery":
            if not self.gallery_screen:
                self.gallery_screen = GalleryScreen(self.container, self.gallery)
            screen = self.gallery_screen
        else:
            raise ValueError("Unknown screen type: {}".format(screen_type))

        # switch to the selected screen if it's not already displayed
        if self.current_screen != screen:
            if self.current_screen:
                self.current_screen.grid_forget()

            self.current_screen = screen
            self.current_screen.grid(row=0, column=0, sticky="nsew")

    def on_closing(self):
        self.root.destroy()

    def create_toast(self,text, auto_close_time = None):
        Toast(self.root, text=text, auto_close_time=auto_close_time)