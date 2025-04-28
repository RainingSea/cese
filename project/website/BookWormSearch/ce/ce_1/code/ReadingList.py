class ReadingList:
    def __init__(self):
        self.reading_list = {}

    def load_reading_list(self):
        with open('reading_list.txt', 'r') as file:
            for line in file:
                username, book_id = line.strip().split('|')
                if username not in self.reading_list:
                    self.reading_list[username] = []
                self.reading_list[username].append(book_id)

    def add_to_reading_list(self, username: str, book_id: str) -> None:
        if username not in self.reading_list:
            self.reading_list[username] = []
        self.reading_list[username].append(book_id)
        with open('reading_list.txt', 'a') as file:
            file.write(f"{username}|{book_id}\n")

    def get_reading_list(self, username: str) -> list:
        return self.reading_list.get(username, [])