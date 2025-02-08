import json

class Theme:
    def __init__(self):
        self.themes = self.load_themes()

    def load_themes(self) -> dict:
        with open('config.json', 'r') as file:
            return json.load(file)

    def get_theme(self, theme_name: str) -> dict:
        return self.themes.get(theme_name, {})