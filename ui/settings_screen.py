import tkinter as tk
import json
from settings_manager import SettingsManager


class SettingsScreen(tk.Frame):
    def __init__(self, master, settings_manager: SettingsManager, on_back):
        super().__init__(master)
        self.on_back = on_back
        self.settings_manager = settings_manager
        
        self.mode_var = tk.StringVar(value=self.settings_manager.get("mode", "manual"))
        tk.Label(self, text="Mode:").grid(row=0, column=0, padx=10, pady=10)
        
        mode_dropdown = tk.OptionMenu(self, self.mode_var, "manual", "automatic")
        mode_dropdown.grid(row=0, column=1, padx=10, pady=10)

        self.save_button = tk.Button(self, text="Save settings", command=self.settings_manager.save_settings)
        self.save_button.grid(row=1, column=0, columnspan=2, pady=5)



    def back_to_main(self):
        self.on_back()  # Callback für die Rücknavigation aufrufen
