class UnitConverter:
    def __init__(self):
        self.conversion_factors = {}

    def load_conversion_factors(self, file_path: str):
        with open(file_path, 'r') as file:
            for line in file:
                unit_type, unit_name, factor = line.strip().split('|')
                if unit_type not in self.conversion_factors:
                    self.conversion_factors[unit_type] = {}
                self.conversion_factors[unit_type][unit_name] = float(factor)

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        from_type = self._get_unit_type(from_unit)
        to_type = self._get_unit_type(to_unit)

        if from_type != to_type:
            raise ValueError("Incompatible unit types for conversion.")

        from_factor = self.conversion_factors[from_type][from_unit]
        to_factor = self.conversion_factors[to_type][to_unit]
        return value * (to_factor / from_factor)

    def _get_unit_type(self, unit: str) -> str:
        for unit_type, units in self.conversion_factors.items():
            if unit in units:
                return unit_type
        raise ValueError(f"Unit '{unit}' not found.")