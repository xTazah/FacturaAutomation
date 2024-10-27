import tkinter as tk
from ui.main_screen import MainScreen
from settings_manager import SettingsManager

class App:
    def __init__(self):
        self.settings_manager = SettingsManager()

        self.root = tk.Tk()
        width = self.settings_manager.get("window_width", 800)
        height = self.settings_manager.get("window_height", 600)
        self.root.geometry(f"{width}x{height}")
        self.root.title("Factura Automation")

        # resize event
        self.root.bind("<Configure>", self.on_resize)

        self.main_screen = MainScreen(self.root, self.settings_manager)

    def on_resize(self, event):
        if event.widget == self.root:
            self.settings_manager.set("window_width", self.root.winfo_width())
            self.settings_manager.set("window_height", self.root.winfo_height())

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
