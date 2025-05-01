import os
from team import Team

class TeamManager:
    def __init__(self):
        self.teams = []

    def add_team(self, team: Team) -> None:
        self.teams.append(team)

    def load_teams(self) -> None:
        if os.path.exists('teams.txt'):
            with open('teams.txt', 'r') as file:
                for line in file:
                    team_data = line.strip().split('|')
                    name = team_data[0]
                    logo = team_data[1]
                    team = Team(name, logo)
                    self.add_team(team)

    def add_player_to_team(self, player) -> None:
        if self.teams:
            self.teams[0].add_player(player)

    def assign_player_to_position(self, player_id: int, position: str) -> None:
        if self.teams:
            self.teams[0].assign_player_to_position(player_id, position)

    def save_teams(self) -> None:
        with open('teams.txt', 'w') as file:
            for team in self.teams:
                file.write(f"{team.name}|{team.logo}\n")