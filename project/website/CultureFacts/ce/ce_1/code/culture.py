class Culture:
    def __init__(self):
        self.cultures = self.load_cultures()

    def load_cultures(self):
        cultures = {}
        with open('cultures.txt', 'r') as file:
            for line in file:
                name, facts = line.strip().split('|')
                cultures[name] = facts
        return cultures

    def get_cultures(self) -> list:
        return list(self.cultures.keys())

    def get_culture_details(self, name: str) -> str:
        return self.cultures.get(name, "Culture not found.")