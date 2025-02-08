class UnitConverter:
    def __init__(self):
        self.conversion_factors = {}

    def load_conversion_factors(self, file_path: str):
        with open(file_path, 'r') as file:
            for line in file:
                unit_type, unit_name, factor = line.strip().split(',')
                self.conversion_factors[(unit_type, unit_name)] = float(factor)

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        from_factor = self.conversion_factors.get(from_unit)
        to_factor = self.conversion_factors.get(to_unit)
        if from_factor is None or to_factor is None:
            raise ValueError("Invalid unit provided for conversion.")
        return value * (to_factor / from_factor)