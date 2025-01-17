class Score:
    def __init__(self):
        self.current_score = 0.0

    def calculate_score(self, drift_precision: float, speed: float, style: float) -> float:
        self.current_score += (drift_precision + speed + style)
        return self.current_score

    def save_score(self, filename: str):
        with open(filename, "a") as file:
            file.write(f"Player|{self.current_score}\n")