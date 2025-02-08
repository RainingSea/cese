class UnitConverter:
    def __init__(self):
        self.conversion_factors = {}

    def load_conversion_factors(self, file_path: str) -> None:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            current_category = None
            for line in lines:
                line = line.strip()
                if line.startswith('#'):
                    current_category = line[1:].strip()
                    self.conversion_factors[current_category] = {}
                elif current_category and line:
                    unit, factor = line.split('|')
                    self.conversion_factors[current_category][unit.strip()] = float(factor.strip())

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        for category, units in self.conversion_factors.items():
            if from_unit in units and to_unit in units:
                return value * (units[to_unit] / units[from_unit])
        raise ValueError(f"Conversion from {from_unit} to {to_unit} is not supported.")