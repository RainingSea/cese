class ReadingList:
    def __init__(self, reading_list_file):
        self.reading_list_file = reading_list_file
        self.load_reading_list()

    def load_reading_list(self):
        self.reading_list = {}
        with open(self.reading_list_file, 'r') as file:
            for line in file:
                username, book_title = line.strip().split('|')
                if username not in self.reading_list:
                    self.reading_list[username] = []
                self.reading_list[username].append(book_title)

    def add_to_reading_list(self, username: str, book_title: str) -> bool:
        if username not in self.reading_list:
            self.reading_list[username] = []
        if book_title in self.reading_list[username]:
            return False
        self.reading_list[username].append(book_title)
        with open(self.reading_list_file, 'a') as file:
            file.write(f"{username}|{book_title}\n")
        return True

    def get_reading_list(self, username: str) -> list:
        return self.reading_list.get(username, [])