import os
from snippet import Snippet

class SnippetManager:
    def __init__(self):
        self.snippets = []

    def load_snippets(self) -> list:
        if not os.path.exists('snippets.txt'):
            return []

        with open('snippets.txt', 'r') as file:
            for line in file:
                content, tags, description = line.strip().split('|')
                snippet = Snippet(content, tags.split(','), description)
                self.snippets.append(snippet)
        return self.snippets

    def save_snippet(self, snippet: Snippet) -> None:
        with open('snippets.txt', 'a') as file:
            file.write(snippet.to_string() + '\n')

    def format_snippet(self, snippet: str) -> str:
        # Basic formatting for demonstration purposes
        return snippet.replace('**', '<b>').replace('__', '<i>')