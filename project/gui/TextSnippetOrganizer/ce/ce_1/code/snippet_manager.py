import json
from snippet import Snippet

class SnippetManager:
    def __init__(self):
        self.snippets = []

    def add_snippet(self, text: str, tags: list, description: str) -> None:
        snippet = Snippet(text, tags, description)
        self.snippets.append(snippet)
        self.save_snippets()

    def load_snippets(self) -> None:
        try:
            with open('snippets.json', 'r') as file:
                data = json.load(file)
                self.snippets = [Snippet(item['text'], item['tags'], item['description']) for item in data]
        except FileNotFoundError:
            self.snippets = []

    def save_snippets(self) -> None:
        with open('snippets.json', 'w') as file:
            json.dump([{'text': snippet.text, 'tags': snippet.tags, 'description': snippet.description} for snippet in self.snippets], file)

    def search_snippets(self, query: str) -> list:
        return [snippet for snippet in self.snippets if query in snippet.text or query in snippet.tags]