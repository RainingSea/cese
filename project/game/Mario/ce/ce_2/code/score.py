class Score:
    def __init__(self):
        self.current_score = 0

    def increase_by_time(self):
        self.current_score += 1

    def increase_on_hit_block(self):
        self.current_score += 10

    def increase_on_touch_mushroom(self):
        self.current_score += 20

    def increase_on_reach_flagpole(self):
        self.current_score += 50