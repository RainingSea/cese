class SleepPatterns:
    def __init__(self):
        self.file_path = 'sleep_patterns.txt'

    def add_pattern(self, pattern: str):
        with open(self.file_path, 'a') as file:
            file.write(pattern + '\n')

    def load_patterns(self):
        with open(self.file_path, 'r') as file:
            return file.read().splitlines()