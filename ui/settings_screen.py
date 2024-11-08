import tkinter as tk
import json
from model.settings_manager import SettingsManager
from ui.utils.button_factory import ButtonFactory


class SettingsScreen(tk.Frame):
    def __init__(self, master, settings_manager: SettingsManager, create_toast):
        super().__init__(master)
        self.settings_manager = settings_manager
        self.create_toast = create_toast
        
        self.mode_var = tk.StringVar(value=self.settings_manager.get("mode", "manual"))
        tk.Label(self, text="Mode:").grid(row=0, column=0, padx=10, pady=10)
        
        mode_dropdown = tk.OptionMenu(self, self.mode_var, "manual", "automatic")
        mode_dropdown.grid(row=0, column=1, padx=10, pady=10)

        self.save_button = ButtonFactory.create_button(self, text="Save settings", onClickHandler=self.save_settings)
        self.save_button.grid(row=1, column=0, columnspan=2, pady=5)

    def save_settings(self):
        self.settings_manager.save_settings()
        self.create_toast("Settings saved", 3000)
