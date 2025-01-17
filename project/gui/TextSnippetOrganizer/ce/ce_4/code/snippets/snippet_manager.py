import json
import os
from snippets.snippet import Snippet

class SnippetManager:
    def __init__(self):
        self.snippets = {}

    def add_snippet(self, content: str, tags: list, description: str):
        tag = tags[0] if tags else "untagged"
        self.snippets[tag] = Snippet(content, tags, description)
        self.save_snippet(tag)

    def edit_snippet(self, tag: str, content: str, tags: list, description: str):
        if tag in self.snippets:
            self.snippets[tag] = Snippet(content, tags, description)
            self.save_snippet(tag)

    def delete_snippet(self, tag: str):
        if tag in self.snippets:
            del self.snippets[tag]
            self.remove_snippet_file(tag)

    def load_snippets(self) -> dict:
        snippets_dir = "snippets/"
        for filename in os.listdir(snippets_dir):
            if filename.endswith(".json"):
                with open(os.path.join(snippets_dir, filename), 'r') as f:
                    data = json.load(f)
                    self.snippets[filename[:-5]] = Snippet(data['content'], data['tags'], data['description'])
        return self.snippets

    def save_snippet(self, tag: str):
        snippet = self.snippets[tag]
        data = {
            'content': snippet.content,
            'tags': snippet.tags,
            'description': snippet.description
        }
        with open(f'snippets/{tag}.json', 'w') as f:
            json.dump(data, f)

    def remove_snippet_file(self, tag: str):
        if os.path.exists(f'snippets/{tag}.json'):
            os.remove(f'snippets/{tag}.json')