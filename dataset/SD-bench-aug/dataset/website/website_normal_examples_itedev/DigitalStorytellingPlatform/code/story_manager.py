class Story:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def save(self):
        with open('stories.txt', 'a') as file:
            file.write(f"{self.title}|{self.content}|{self.author}\n")

class StoryManager:
    def __init__(self, stories_file: str):
        self.stories_file = stories_file
        self.load_stories()

    def load_stories(self):
        self.stories = []
        try:
            with open(self.stories_file, 'r') as file:
                for line in file:
                    title, content, author = line.strip().split('|')
                    self.stories.append(Story(title, content, author))
        except FileNotFoundError:
            open(self.stories_file, 'w').close()  # Create file if it doesn't exist

    def create_story(self, title: str, content: str, author: str):
        new_story = Story(title, content, author)
        new_story.save()
        self.stories.append(new_story)

    def edit_story(self, title: str, content: str):
        for story in self.stories:
            if story.title == title:
                story.content = content
                self.save_all_stories()
                break

    def save_all_stories(self):
        with open(self.stories_file, 'w') as file:
            for story in self.stories:
                file.write(f"{story.title}|{story.content}|{story.author}\n")