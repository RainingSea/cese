class Culture:
    def __init__(self, name: str = '', facts: str = ''):
        self.name = name
        self.facts = facts

    @staticmethod
    def load_cultures():
        cultures = []
        try:
            with open('cultures.txt', 'r') as f:
                for line in f:
                    name, facts = line.strip().split('|')
                    cultures.append(Culture(name, facts))
        except FileNotFoundError:
            pass
        return cultures