class Recipe:
    def __init__(self, title: str, ingredients: str, instructions: str):
        self.title = title
        self.ingredients = ingredients
        self.instructions = instructions

    def to_string(self) -> str:
        return f"{self.title}|{self.ingredients}|{self.instructions}"