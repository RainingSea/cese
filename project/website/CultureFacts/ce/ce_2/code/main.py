class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append((username, password))
        except FileNotFoundError:
            pass
        return users

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append((username, password))
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user[0] == username and user[1] == password for user in self.users)


class CultureManager:
    def __init__(self):
        self.cultures = self.load_cultures()

    def load_cultures(self):
        cultures = []
        try:
            with open('cultures.txt', 'r') as file:
                for line in file:
                    cultures.append(line.strip())
        except FileNotFoundError:
            pass
        return cultures

    def get_cultures(self) -> list:
        return self.cultures

    def get_culture_details(self, culture_name: str) -> str:
        for culture in self.cultures:
            if culture.startswith(culture_name):
                return culture
        return "Culture not found."

    def search_cultures(self, query: str) -> list:
        return [culture for culture in self.cultures if query.lower() in culture.lower()]


class BookmarkManager:
    def __init__(self):
        self.bookmarks = self.load_bookmarks()

    def load_bookmarks(self):
        bookmarks = []
        try:
            with open('bookmarks.txt', 'r') as file:
                for line in file:
                    bookmarks.append(line.strip())
        except FileNotFoundError:
            pass
        return bookmarks

    def add_bookmark(self, culture_name: str) -> bool:
        if culture_name in self.bookmarks:
            return False
        self.bookmarks.append(culture_name)
        with open('bookmarks.txt', 'a') as file:
            file.write(f"{culture_name}\n")
        return True

    def remove_bookmark(self, culture_name: str) -> bool:
        if culture_name in self.bookmarks:
            self.bookmarks.remove(culture_name)
            with open('bookmarks.txt', 'w') as file:
                for bookmark in self.bookmarks:
                    file.write(f"{bookmark}\n")
            return True
        return False

    def get_bookmarks(self) -> list:
        return self.bookmarks


class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.culture_manager = CultureManager()
        self.bookmark_manager = BookmarkManager()

    def main(self):
        # Placeholder for the main application logic
        pass


if __name__ == "__main__":
    app = Main()
    app.main()