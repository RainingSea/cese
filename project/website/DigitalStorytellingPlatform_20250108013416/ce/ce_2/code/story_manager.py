class StoryManager:
    def __init__(self, stories_file: str):
        self.stories_file = stories_file

    def create_story(self, username: str, title: str, content: str) -> None:
        with open(self.stories_file, 'a') as f:
            f.write(f"{username}:{title}:{content}\n")

    def load_stories(self, username: str) -> list:
        stories = []
        try:
            with open(self.stories_file, 'r') as f:
                for line in f:
                    user, title, content = line.strip().split(':')
                    if user == username:
                        stories.append({'title': title, 'content': content})
        except FileNotFoundError:
            pass
        return stories