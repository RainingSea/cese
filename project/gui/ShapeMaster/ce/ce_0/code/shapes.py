class Shape:
    def __init__(self, type: str, properties: dict):
        self.type = type
        self.properties = properties

    def set_properties(self, properties: dict):
        self.properties = properties

    def get_properties(self) -> dict:
        return self.properties


class Rectangle:
    def __init__(self, properties: dict):
        self.shape = Shape("Rectangle", properties)


class Circle:
    def __init__(self, properties: dict):
        self.shape = Shape("Circle", properties)


class Triangle:
    def __init__(self, properties: dict):
        self.shape = Shape("Triangle", properties)


class Polygon:
    def __init__(self, properties: dict):
        self.shape = Shape("Polygon", properties)