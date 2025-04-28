class CultureManager:
    def __init__(self):
        self.cultures = self.load_cultures()

    def load_cultures(self):
        cultures = []
        try:
            with open('cultures.txt', 'r') as file:
                for line in file:
                    cultures.append(line.strip())
        except FileNotFoundError:
            pass
        return cultures

    def get_all_cultures(self):
        return self.cultures

    def get_culture_details(self, culture_name: str) -> str:
        for culture in self.cultures:
            if culture.startswith(culture_name):
                return culture
        return "Culture not found."

    def search_cultures(self, keyword: str):
        return [culture for culture in self.cultures if keyword.lower() in culture.lower()]