import json

class SnippetManager:
    def __init__(self):
        self.snippets = []

    def add_snippet(self, snippet: str, tags: list, description: str) -> None:
        self.snippets.append({
            "snippet": snippet,
            "tags": tags,
            "description": description
        })
        self.save_snippets()

    def search_snippet(self, query: str) -> list:
        return [s['snippet'] for s in self.snippets if query.lower() in s['snippet'].lower()]

    def load_snippets(self) -> None:
        try:
            with open('snippets.txt', 'r') as file:
                data = json.load(file)
                self.snippets = data.get('snippets', [])
        except FileNotFoundError:
            self.snippets = []

    def save_snippets(self) -> None:
        with open('snippets.txt', 'w') as file:
            json.dump({"snippets": self.snippets}, file)