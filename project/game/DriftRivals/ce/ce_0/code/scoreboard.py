from score import Score

class Scoreboard:
    def __init__(self):
        self.scores = []
        self.load_scores()

    def add_score(self, player_name: str, score: int):
        new_score = Score(player_name, score)
        self.scores.append(new_score)
        self.save_scores()

    def load_scores(self):
        try:
            with open('scores.txt', 'r') as file:
                for line in file:
                    player_name, score_value = line.strip().split('|')
                    self.scores.append(Score(player_name, int(score_value)))
        except FileNotFoundError:
            pass

    def save_scores(self):
        with open('scores.txt', 'w') as file:
            for score in self.scores:
                file.write(f"{score.player_name}|{score.score_value}\n")