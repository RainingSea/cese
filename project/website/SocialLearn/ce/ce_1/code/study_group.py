import os

class StudyGroup:
    def __init__(self, group_name: str):
        self.group_name = group_name
        self.members = []

    def add_member(self, username: str):
        self.members.append(username)
        self.save()

    def save(self):
        with open('groups.txt', 'a') as file:
            file.write(f"{self.group_name}|{','.join(self.members)}\n")