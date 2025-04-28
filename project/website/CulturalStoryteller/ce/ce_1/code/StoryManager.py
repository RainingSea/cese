class StoryManager:
    def __init__(self):
        self.stories = []
        self.load_stories()

    def load_stories(self) -> None:
        try:
            with open('stories.txt', 'r') as file:
                for line in file:
                    title, cultural_origin, category, text = line.strip().split(',')
                    self.stories.append({
                        'title': title,
                        'cultural_origin': cultural_origin,
                        'category': category,
                        'text': text
                    })
        except FileNotFoundError:
            pass

    def save_stories(self) -> None:
        with open('stories.txt', 'w') as file:
            for story in self.stories:
                file.write(f"{story['title']},{story['cultural_origin']},{story['category']},{story['text']}\n")

    def search_stories(self, query: str) -> list:
        return [story for story in self.stories if query.lower() in story['title'].lower()]

    def bookmark_story(self, username: str, title: str) -> None:
        with open('bookmarks.txt', 'a') as file:
            file.write(f"{username},{title}\n")

    def get_bookmarks(self, username: str) -> list:
        bookmarks = []
        try:
            with open('bookmarks.txt', 'r') as file:
                for line in file:
                    user, title = line.strip().split(',')
                    if user == username:
                        bookmarks.append(title)
        except FileNotFoundError:
            pass
        return bookmarks