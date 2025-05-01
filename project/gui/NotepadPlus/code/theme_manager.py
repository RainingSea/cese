import json

class ThemeManager:
    def __init__(self):
        self.themes = {}

    def load_themes(self) -> None:
        try:
            with open('settings.txt', 'r') as file:
                for line in file:
                    name, background, foreground = line.strip().split('|')
                    self.themes[name] = {'background': background, 'foreground': foreground}
        except FileNotFoundError:
            print("Settings file not found. Using default theme.")

    def get_theme(self, theme_name: str) -> dict:
        return self.themes.get(theme_name, self.themes.get("default", {}))