import os

class Converter:
    def __init__(self):
        self.conversion_rates = {}
        self.load_conversion_rates()

    def load_conversion_rates(self):
        """Load conversion rates from a file."""
        if os.path.exists('conversion_rates.txt'):
            with open('conversion_rates.txt', 'r') as file:
                for line in file:
                    from_unit, to_unit, rate = line.strip().split('|')
                    self.conversion_rates[(from_unit, to_unit)] = float(rate)

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert value from one unit to another using the conversion rates."""
        if (from_unit, to_unit) in self.conversion_rates:
            return value * self.conversion_rates[(from_unit, to_unit)]
        elif (from_unit, to_unit) == ('celsius', 'fahrenheit'):
            return (value * 1.8) + 32
        elif (from_unit, to_unit) == ('fahrenheit', 'celsius'):
            return (value - 32) * 0.5556
        else:
            raise ValueError("Conversion rate not found.")

    def save_conversion_history(self, value: float, from_unit: str, to_unit: str, result: float):
        """Save the conversion history to a file."""
        with open('conversion_history.txt', 'a') as file:
            file.write(f"{value}|{from_unit}|{to_unit}|{result:.4f}\n")

    def get_conversion_history(self):
        """Retrieve the conversion history from the file."""
        try:
            with open('conversion_history.txt', 'r') as file:
                history = [line.strip() for line in file.readlines()]
                return history
        except FileNotFoundError:
            return []

    def get_available_units(self):
        """Retrieve a list of unique units available for conversion."""
        units = set()
        for from_unit, to_unit in self.conversion_rates.keys():
            units.add(from_unit)
            units.add(to_unit)
        return list(units)

    def get_conversion_options(self):
        """Retrieve a list of available conversion options."""
        return [(from_unit, to_unit) for from_unit, to_unit in self.conversion_rates.keys()]