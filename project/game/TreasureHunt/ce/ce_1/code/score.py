class Score:
    def __init__(self):
        self.current_score = 0
        self.best_time = float('inf')

    def increase(self):
        self.current_score += 1

    def save_score(self):
        with open('scores.txt', 'a') as f:
            f.write(f'player_name,{self.current_score}\n')