class CultureManager:
    def __init__(self, cultures_file: str):
        self.cultures_file = cultures_file
        self.cultures = self.load_cultures()

    def load_cultures(self) -> list:
        cultures = []
        try:
            with open(self.cultures_file, 'r') as f:
                for line in f:
                    cultures.append(line.strip())
        except FileNotFoundError:
            pass
        return cultures

    def get_culture_details(self, culture_name: str) -> dict:
        details = {}
        try:
            with open(self.cultures_file, 'r') as f:
                for line in f:
                    name, description = line.strip().split('|')
                    if name == culture_name:
                        details['name'] = name
                        details['description'] = description
                        break
        except FileNotFoundError:
            pass
        return details