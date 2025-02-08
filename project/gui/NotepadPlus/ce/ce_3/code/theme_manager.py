class ThemeManager:
    def __init__(self):
        self.available_themes = {}
        self.load_themes()

    def load_themes(self):
        # Predefined themes for demonstration
        self.available_themes = {
            "light": {
                "background": "#ffffff",
                "foreground": "#000000",
                "font": "Arial"
            },
            "dark": {
                "background": "#000000",
                "foreground": "#ffffff",
                "font": "Courier"
            }
        }

    def get_theme(self, theme_name: str) -> dict:
        return self.available_themes.get(theme_name, self.available_themes["light"])