class Culture:
    """Represents a culture with its facts."""
    
    def __init__(self, name: str, facts: list):
        self.name = name
        self.facts = facts

    @staticmethod
    def load_cultures() -> list:
        """Loads cultures from the cultures file."""
        cultures = []
        with open('cultures.txt', 'r') as f:
            for line in f:
                culture_data = line.strip().split('|')
                cultures.append(Culture(culture_data[0], culture_data[1:]))
        return cultures

    def get_details(self) -> str:
        """Returns a string representation of the culture details."""
        return f"Culture: {self.name}\nFacts: {', '.join(self.facts)}"