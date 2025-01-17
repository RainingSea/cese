class UnitConverter:
    def __init__(self):
        self.conversion_factors = {}

    def load_conversion_factors(self, file_path: str) -> None:
        with open(file_path, 'r') as file:
            for line in file:
                from_unit, to_unit, factor = line.strip().split('|')
                self.conversion_factors[(from_unit, to_unit)] = eval(factor)

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        if (from_unit, to_unit) in self.conversion_factors:
            factor = self.conversion_factors[(from_unit, to_unit)]
            return value * factor
        else:
            raise ValueError(f"Conversion from {from_unit} to {to_unit} not supported.")