import json
import os

class TacticsManager:
    def __init__(self):
        self.tactics = {}
        self.load_tactics()

    def load_tactics(self) -> None:
        if os.path.exists('tactics.json'):
            with open('tactics.json', 'r') as file:
                self.tactics = json.load(file)

    def create_tactic(self, name: str, details: dict) -> None:
        self.tactics[name] = details
        self.save_tactics()

    def save_tactics(self) -> None:
        with open('tactics.json', 'w') as file:
            json.dump(self.tactics, file)