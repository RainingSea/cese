class CultureManager:
    def __init__(self):
        self.cultures = []

    def load_cultures(self) -> None:
        try:
            with open('cultures.txt', 'r') as file:
                self.cultures = file.read().strip().splitlines()
        except FileNotFoundError:
            self.cultures = []

    def get_culture_details(self, culture_name: str) -> str:
        for culture in self.cultures:
            if culture.split('|')[0] == culture_name:
                return culture
        return "Culture not found."

    def search_cultures(self, keyword: str) -> list:
        return [culture for culture in self.cultures if keyword.lower() in culture.lower()]