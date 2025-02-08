import json
import os
from snippets.snippet import Snippet

class SnippetManager:
    def __init__(self):
        self.snippets = {}

    def add_snippet(self, text: str, tags: list, description: str):
        snippet = Snippet(text, tags, description)
        for tag in tags:
            if tag not in self.snippets:
                self.snippets[tag] = []
            self.snippets[tag].append(snippet)
        self.save_snippets()

    def get_snippets_by_tag(self, tag: str) -> list:
        return self.snippets.get(tag, [])

    def save_snippets(self):
        for tag, snippets in self.snippets.items():
            filename = f'snippets/{tag}.json'
            with open(filename, 'w') as f:
                json_data = [{'text': snippet.text, 'tags': snippet.tags, 'description': snippet.description} for snippet in snippets]
                json.dump(json_data, f, indent=4)

    def load_snippets(self):
        for filename in os.listdir('snippets'):
            if filename.endswith('.json'):
                with open(os.path.join('snippets', filename), 'r') as f:
                    snippets_data = json.load(f)
                    tag = filename[:-5]  # Remove .json
                    self.snippets[tag] = [Snippet(item['text'], item['tags'], item['description']) for item in snippets_data]