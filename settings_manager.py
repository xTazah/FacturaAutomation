import json

class SettingsManager:
    def __init__(self, filepath="settings.json"):
        self.filepath = filepath
        self.settings = self.load_settings()

    def load_settings(self):
        try:
            with open(self.filepath, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            # Standardwerte
            return {"window_width": 800, "window_height": 600, "mode": "manual"}

    def save_settings(self):
        with open(self.filepath, "w") as file:
            json.dump(self.settings, file, indent=4)

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()
