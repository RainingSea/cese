class CultureManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.cultures = self.load_cultures()

    def load_cultures(self) -> dict:
        """Loads cultures from the specified file."""
        cultures = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    name, details = line.strip().split('|')
                    cultures[name] = details
        except FileNotFoundError:
            pass
        return cultures

    def get_culture_details(self, culture_name: str) -> dict:
        """Retrieves details for a specific culture."""
        return {culture_name: self.cultures.get(culture_name, "Details not found")}