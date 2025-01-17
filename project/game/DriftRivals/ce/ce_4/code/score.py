class Score:
    def __init__(self):
        self.current_score = 0

    def calculate_score(self, precision, speed, style):
        self.current_score += int(precision * speed * style)
        return self.current_score

    def save_score_to_file(self, filename):
        with open(filename, 'a') as file:
            file.write(f"{self.current_score}\n")