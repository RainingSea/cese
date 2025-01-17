class Settings:
    def __init__(self):
        self.settings = {
            "volume": 0.5,
            "difficulty": "normal"
        }

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            for key, value in self.settings.items():
                file.write(f"{key}|{value}\n")

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                key, value = line.strip().split('|')
                self.settings[key] = value