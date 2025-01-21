class Culture:
    def __init__(self, name: str, facts: str):
        self.name = name
        self.facts = facts

    @staticmethod
    def load_all() -> list:
        cultures = []
        with open('cultures.txt', 'r') as file:
            for line in file:
                name, facts = line.strip().split('|')
                cultures.append(Culture(name, facts))
        return cultures