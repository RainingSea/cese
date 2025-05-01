import json

class Theme:
    def __init__(self):
        self.name = ""
        self.background_color = ""
        self.text_color = ""

    def load_theme(self) -> None:
        try:
            with open('config.txt', 'r') as config_file:
                theme_data = config_file.read().strip()
                self.name, self.background_color, self.text_color = theme_data.split('|')
                # Apply the theme settings to the text editor (placeholder)
        except Exception as e:
            print(f"Error loading theme: {e}")