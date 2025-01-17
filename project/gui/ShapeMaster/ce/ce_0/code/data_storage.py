import json

def save_shapes(shapes: list, filename: str = 'shapes.json'):
    with open(filename, 'w') as file:
        json.dump([shape.get_properties() for shape in shapes], file)

def load_shapes(filename: str = 'shapes.json') -> list:
    try:
        with open(filename, 'r') as file:
            shapes_data = json.load(file)
            return [Shape(shape['type'], shape) for shape in shapes_data]
    except FileNotFoundError:
        return []

def save_preferences(preferences: dict, filename: str = 'preferences.json'):
    with open(filename, 'w') as file:
        json.dump(preferences, file)

def load_preferences(filename: str = 'preferences.json') -> dict:
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}