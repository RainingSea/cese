import os
from typing import List

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.entry_manager = EntryManager()

    def main(self) -> str:
        return "Travel_Log application started."

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self) -> List[str]:
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as file:
            return [line.strip().split(',') for line in file.readlines()]

    def register(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username:
                return False  # User already exists
        self.users.append([username, password])
        self.save_users()
        return True

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(','.join(user) + '\n')

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                return True
        return False

class EntryManager:
    def __init__(self):
        self.entries = self.load_entries()

    def load_entries(self) -> List[str]:
        if not os.path.exists('entries.txt'):
            return []
        with open('entries.txt', 'r') as file:
            return [line.strip().split(',') for line in file.readlines()]

    def create_entry(self, username: str, destination: str, dates: str, activities: str, photos: str, reflections: str) -> bool:
        entry = [username, destination, dates, activities, photos, reflections]
        self.entries.append(entry)
        self.save_entries()
        return True

    def save_entries(self):
        with open('entries.txt', 'w') as file:
            for entry in self.entries:
                file.write(','.join(entry) + '\n')

    def view_entries(self, username: str) -> List:
        return [entry for entry in self.entries if entry[0] == username]

    def edit_entry(self, entry_id: int, new_data: dict) -> bool:
        if 0 <= entry_id < len(self.entries):
            self.entries[entry_id] = [
                new_data.get('username', self.entries[entry_id][0]),
                new_data.get('destination', self.entries[entry_id][1]),
                new_data.get('dates', self.entries[entry_id][2]),
                new_data.get('activities', self.entries[entry_id][3]),
                new_data.get('photos', self.entries[entry_id][4]),
                new_data.get('reflections', self.entries[entry_id][5])
            ]
            self.save_entries()
            return True
        return False

    def delete_entry(self, entry_id: int) -> bool:
        if 0 <= entry_id < len(self.entries):
            del self.entries[entry_id]
            self.save_entries()
            return True
        return False

    def search_entries(self, query: str) -> List:
        return [entry for entry in self.entries if query in entry]