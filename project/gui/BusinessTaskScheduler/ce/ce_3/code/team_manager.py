import json
from typing import List

class User:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

class TeamManager:
    def __init__(self):
        self.team_members = []

    def load_team_members(self) -> None:
        try:
            with open('team_members.txt', 'r') as file:
                self.team_members = [User(*line.strip().split('|')) for line in file.readlines()]
        except FileNotFoundError:
            self.team_members = []

    def save_team_members(self) -> None:
        with open('team_members.txt', 'w') as file:
            for member in self.team_members:
                file.write(f"{member.name}|{member.role}\n")

    def add_member(self, user: User) -> None:
        self.team_members.append(user)
        self.save_team_members()

    def get_members(self) -> List[User]:
        return self.team_members