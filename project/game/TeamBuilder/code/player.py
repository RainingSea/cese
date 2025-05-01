class Player:
    def __init__(self, player_id: int, name: str, stats: dict):
        self.id = player_id
        self.name = name
        self.stats = stats
        self.position = None

    def update_stats(self, new_stats: dict) -> None:
        self.stats.update(new_stats)

    def train(self, exercise: str) -> None:
        if exercise == "speed":
            self.stats['speed'] += 1
        elif exercise == "strength":
            self.stats['strength'] += 1