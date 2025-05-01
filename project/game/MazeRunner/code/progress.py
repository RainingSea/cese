class Progress:
    def __init__(self):
        self.progress_data = {}

    def load_progress(self, player_name: str):
        try:
            with open("progress.txt", "r") as file:
                for line in file:
                    name, level, score = line.strip().split('|')
                    self.progress_data[name] = {'level': level, 'score': int(score)}
        except FileNotFoundError:
            pass  # If the file does not exist, start with an empty progress

    def update_progress(self, player_name: str, score: int):
        if player_name in self.progress_data:
            self.progress_data[player_name]['score'] = score
        else:
            self.progress_data[player_name] = {'level': 'level1', 'score': score}
        self.save_progress()

    def save_progress(self):
        with open("progress.txt", "w") as file:
            for name, data in self.progress_data.items():
                file.write(f"{name}|{data['level']}|{data['score']}\n")