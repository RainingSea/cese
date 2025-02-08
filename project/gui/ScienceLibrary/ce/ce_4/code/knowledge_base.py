import json

class KnowledgeBase:
    def fetch_data(self):
        with open('articles.json', 'r') as file:
            return json.load(file)