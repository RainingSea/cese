import os
from snippet import Snippet

class SnippetManager:
    def __init__(self):
        self.snippets = []

    def add_snippet(self, snippet_text: str, tags: list, description: str) -> None:
        snippet = Snippet(snippet_text, tags, description)
        self.snippets.append(snippet)
        self.save_snippets()

    def search_snippets(self, tag: str) -> list:
        return [snippet for snippet in self.snippets if tag in snippet.tags]

    def load_snippets(self) -> None:
        if os.path.exists("snippets.txt"):
            with open("snippets.txt", "r") as file:
                for line in file:
                    text, tags, description = line.strip().split('|')
                    tags_list = tags.split(',')
                    self.snippets.append(Snippet(text, tags_list, description))

    def save_snippets(self) -> None:
        with open("snippets.txt", "w") as file:
            for snippet in self.snippets:
                file.write(f"{snippet.text}|{','.join(snippet.tags)}|{snippet.description}\n")