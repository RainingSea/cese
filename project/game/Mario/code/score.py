class Score:
    def __init__(self):
        self.scores = []

    def save_to_file(self, filename):
        with open(filename, 'a') as file:
            file.write(f"{self.scores[-1]}\n")  # Save only the latest score

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            self.scores = [int(line.strip()) for line in file.readlines()]