class Score:
    def __init__(self):
        self.points = 0

    def update_score(self, points: int):
        self.points += points
        print(f"Score updated: {self.points}")

    def save_high_score(self, name: str):
        with open('high_scores.txt', 'a') as file:
            file.write(f"{name}|{self.points}\n")

    def get_score(self):
        return self.points

    def view_high_scores(self):
        with open('high_scores.txt', 'r') as file:
            scores = file.readlines()
            print("High Scores:")
            for score in scores:
                print(score.strip())