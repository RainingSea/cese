class CultureManager:
    def __init__(self, cultures_file: str):
        self.cultures_file = cultures_file
        self.load_cultures()

    def load_cultures(self):
        self.cultures = {}
        with open(self.cultures_file, 'r') as file:
            for line in file:
                culture_name, facts = line.strip().split('|')
                self.cultures[culture_name] = facts

    def get_cultures(self) -> list:
        return list(self.cultures.keys())

    def get_culture_details(self, culture_name: str) -> str:
        return self.cultures.get(culture_name, "Culture not found.")

    def search_cultures(self, query: str) -> list:
        return [name for name in self.cultures if query.lower() in name.lower()]