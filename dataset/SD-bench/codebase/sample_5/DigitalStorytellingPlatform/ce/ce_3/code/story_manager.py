class Story:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

class StoryManager:
    def __init__(self):
        self.stories = self.load_stories()

    def save_story(self, title: str, content: str) -> None:
        new_story = Story(title, content)
        self.stories.append(new_story)
        self.save_stories()

    def load_stories(self) -> list:
        stories = []
        try:
            with open('stories.txt', 'r') as file:
                for line in file:
                    title, content = line.strip().split('|')
                    stories.append(Story(title, content))
        except FileNotFoundError:
            pass
        return stories

    def save_stories(self) -> None:
        with open('stories.txt', 'w') as file:
            for story in self.stories:
                file.write(f"{story.title}|{story.content}\n")