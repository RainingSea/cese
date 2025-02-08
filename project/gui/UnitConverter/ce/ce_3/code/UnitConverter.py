class UnitConverter:
    def __init__(self):
        self.units = {}
        self.conversion_history = []

    def load_units(self, file_path: str):
        with open(file_path, 'r') as file:
            for line in file:
                unit, factor = line.strip().split('|')
                self.units[unit] = float(factor)

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        if from_unit in self.units and to_unit in self.units:
            return value * (self.units[to_unit] / self.units[from_unit])
        raise ValueError("Invalid units for conversion.")

    def save_history(self, value: float, from_unit: str, to_unit: str, result: float):
        history_entry = f"{value} {from_unit} to {to_unit} = {result}\n"
        self.conversion_history.append(history_entry)
        with open('history.txt', 'a') as file:
            file.write(history_entry)

    def display_history(self) -> list:
        return self.conversion_history