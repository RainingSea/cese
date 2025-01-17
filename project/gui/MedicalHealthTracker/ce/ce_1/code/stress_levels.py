class StressLevels:
    def __init__(self):
        self.file_path = 'stress_levels.txt'

    def add_stress(self, level: str):
        with open(self.file_path, 'a') as file:
            file.write(level + '\n')

    def load_stress(self):
        with open(self.file_path, 'r') as file:
            return file.read().splitlines()