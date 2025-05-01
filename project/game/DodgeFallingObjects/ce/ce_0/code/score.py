class Score:
    def load_scores(self):
        scores = []
        with open('scores.txt', 'r') as file:
            for line in file:
                scores.append(int(line.strip()))
        return scores

    def write_score(self, score):
        with open('scores.txt', 'a') as file:
            file.write(f"{score}\n")