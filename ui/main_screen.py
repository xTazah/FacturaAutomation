import tkinter as tk
from tkinter import PhotoImage
from ui.camera_screen import CameraScreen
from ui.settings_screen import SettingsScreen
from ui.gallery_screen import GalleryScreen
from ui.toast import Toast
from button_factory import ButtonFactory
from settings_manager import SettingsManager
from camera import Camera
from gallery import Gallery

class MainScreen:
    def __init__(self, root, settings_manager: SettingsManager, camera: Camera, gallery: Gallery):
        self.root = root
        self.root.title("Camera Scanner")
        self.settings_manager = settings_manager
        self.camera = camera
        self.gallery = gallery

        self.camera_screen = None
        self.settings_screen = None

        self.create_navigation()

        # container that holds the different screens
        self.container = tk.Frame(root, height=800, width=800)
        self.container.pack()

        # show camera screen at startup
        self.current_screen = None
        self.show_camera_screen()

    def create_navigation(self):
        nav_frame = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=10)
        nav_frame.pack(side=tk.TOP, fill=tk.X)

        self.camera_icon = PhotoImage(file="ui/icons/camera.png")
        self.settings_icon = PhotoImage(file="ui/icons/settings.png")
        self.gallery_icon = PhotoImage(file="ui/icons/gallery.png")

        # Creating the buttons with grid layout to simulate space-between
        ButtonFactory.create_button(nav_frame, icon=self.gallery_icon, onClickHandler=self.show_gallery_screen, column=0, row=0)
        ButtonFactory.create_button(nav_frame, icon=self.camera_icon, onClickHandler=self.show_camera_screen, column=1, row=0)
        ButtonFactory.create_button(nav_frame, icon=self.settings_icon, onClickHandler=self.show_settings_screen, column=2, row=0)

        # Adjusting column weights to achieve space-between effect
        nav_frame.grid_columnconfigure(0, weight=1)
        nav_frame.grid_columnconfigure(1, weight=1)
        nav_frame.grid_columnconfigure(2, weight=1)

    def show_camera_screen(self):
        if not self.camera_screen:
                self.camera_screen = CameraScreen(self.container, self.camera, self.gallery)

        if self.current_screen != self.camera_screen:
            
            if self.current_screen:
                self.current_screen.grid_forget()

            self.current_screen = self.camera_screen
            self.current_screen.grid(row=0, column=0)

    def show_settings_screen(self):
        if not self.settings_screen:
            self.settings_screen = SettingsScreen(self.container, self.settings_manager, self.create_toast)

        if self.current_screen != self.settings_screen:

            if self.current_screen:
                self.current_screen.grid_forget()

            self.current_screen = self.settings_screen
            self.current_screen.grid(row=0, column=0)

    def show_gallery_screen(self):
        if not self.settings_screen:
            self.settings_screen = GalleryScreen(self.container, self.gallery)

        if self.current_screen != self.settings_screen:

            if self.current_screen:
                self.current_screen.grid_forget()

            self.current_screen = self.settings_screen
            self.current_screen.grid(row=0, column=0)

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def on_closing(self):
        self.root.destroy()

    def create_toast(self,text, auto_close_time = None):
        Toast(self.root, text=text, auto_close_time=auto_close_time)