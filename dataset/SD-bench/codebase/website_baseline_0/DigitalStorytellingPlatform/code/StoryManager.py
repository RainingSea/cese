class Story:
    def __init__(self, username: str, title: str, content: str):
        self.username = username
        self.title = title
        self.content = content

    def save(self) -> None:
        with open('stories.txt', 'a') as file:
            file.write(f"{self.username},{self.title},{self.content}\n")


class StoryManager:
    def __init__(self, stories_file: str = 'stories.txt'):
        self.stories_file = stories_file
        self.stories = self.load_stories()

    def create_story(self, username: str, title: str, content: str) -> None:
        story = Story(username, title, content)
        story.save()
        self.stories.append(story)

    def load_stories(self) -> list:
        stories = []
        try:
            with open(self.stories_file, 'r') as file:
                for line in file:
                    username, title, content = line.strip().split(',', 2)
                    stories.append(Story(username, title, content))
        except FileNotFoundError:
            pass  # No stories file found
        return stories

    def edit_story(self, username: str, title: str, new_title: str, new_content: str) -> None:
        for story in self.stories:
            if story.username == username and story.title == title:
                story.title = new_title
                story.content = new_content
                self.save_all_stories()
                break

    def save_all_stories(self) -> None:
        with open(self.stories_file, 'w') as file:
            for story in self.stories:
                file.write(f"{story.username},{story.title},{story.content}\n")