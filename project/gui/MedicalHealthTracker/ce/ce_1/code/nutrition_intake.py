class NutritionIntake:
    def __init__(self):
        self.file_path = 'nutrition_intake.txt'

    def add_nutrition(self, nutrition: str):
        with open(self.file_path, 'a') as file:
            file.write(nutrition + '\n')

    def load_nutrition(self):
        with open(self.file_path, 'r') as file:
            return file.read().splitlines()