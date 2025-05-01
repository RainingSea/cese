import json

class AnnotationManager:
    def __init__(self):
        self.annotations = self.load_annotations()

    def create_annotation(self, article: str, note: str):
        if article not in self.annotations:
            self.annotations[article] = []
        self.annotations[article].append(note)
        self.save_annotations()

    def load_annotations(self):
        try:
            with open('annotations.txt', 'r') as file:
                annotations = {}
                for line in file:
                    article, note = line.strip().split('|')
                    if article in annotations:
                        annotations[article].append(note)
                    else:
                        annotations[article] = [note]
                return annotations
        except FileNotFoundError:
            return {}

    def save_annotations(self):
        with open('annotations.txt', 'w') as file:
            for article, notes in self.annotations.items():
                for note in notes:
                    file.write(f"{article}|{note}\n")