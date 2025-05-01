class Converter:
    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        conversion_factors = {
            'meters': 1.0,
            'kilometers': 0.001,
            'centimeters': 100.0,
            'millimeters': 1000.0,
            'miles': 0.000621371,
            'yards': 1.09361,
            'feet': 3.28084,
        }
        
        if from_unit not in conversion_factors or to_unit not in conversion_factors:
            raise ValueError("Invalid unit provided for conversion.")
        
        # Convert from the original unit to meters, then to the target unit
        value_in_meters = value / conversion_factors[from_unit]
        converted_value = value_in_meters * conversion_factors[to_unit]
        return converted_value

    def get_conversion_history(self) -> list:
        try:
            with open('conversion_history.txt', 'r') as file:
                history = file.readlines()
            return [entry.strip() for entry in history]
        except FileNotFoundError:
            return []

    def save_conversion(self, original_value: float, original_unit: str, converted_value: float, converted_unit: str) -> None:
        with open('conversion_history.txt', 'a') as file:
            entry = f"{original_value} {original_unit} {converted_value} {converted_unit}\n"
            file.write(entry)