class PowerUp:
    def __init__(self, effect_type: str):
        self.effect_type = effect_type
        self.active = True

    def is_active(self) -> bool:
        return self.active

    def apply_effect(self, game):
        if self.effect_type == "double_score":
            game.update_score(game.score.get_score())  # Double the score
            self.active = False  # Deactivate after use
        # Additional effects can be added here