class Culture:
    def __init__(self, name: str, facts: list):
        self.name = name
        self.facts = facts

    def get_details(self) -> dict:
        return {
            'name': self.name,
            'facts': self.facts
        }