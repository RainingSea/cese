import os

class DataStorage:
    WORD_LIST_FILE = 'word_list.txt'
    SCORES_FILE = 'scores.txt'

    @staticmethod
    def load_word_list():
        if not os.path.exists(DataStorage.WORD_LIST_FILE):
            return []
        with open(DataStorage.WORD_LIST_FILE, 'r') as file:
            return [line.strip() for line in file.readlines()]

    @staticmethod
    def save_score(player_name, score):
        with open(DataStorage.SCORES_FILE, 'a') as file:
            file.write(f"{player_name}|{score}\n")

    @staticmethod
    def load_scores():
        if not os.path.exists(DataStorage.SCORES_FILE):
            return {}
        scores = {}
        with open(DataStorage.SCORES_FILE, 'r') as file:
            for line in file:
                name, score = line.strip().split('|')
                scores[name] = int(score)
        return scores