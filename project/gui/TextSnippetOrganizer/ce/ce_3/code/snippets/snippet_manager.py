import os

class SnippetManager:
    def __init__(self, snippet_directory='snippets'):
        self.snippet_directory = snippet_directory
        if not os.path.exists(snippet_directory):
            os.makedirs(snippet_directory)

    def save_snippet(self, tag: str, snippet: str, description: str) -> None:
        filename = os.path.join(self.snippet_directory, f"{tag}.txt")
        with open(filename, 'w') as file:
            file.write(snippet + '\n' + description)

    def retrieve_snippet(self, tag: str) -> dict:
        filename = os.path.join(self.snippet_directory, f"{tag}.txt")
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                lines = file.readlines()
                snippet = lines[0].strip()
                description = lines[1].strip()
                return {'snippet': snippet, 'description': description}
        return {}

    def list_snippets(self) -> list:
        return [f[:-4] for f in os.listdir(self.snippet_directory) if f.endswith('.txt')]