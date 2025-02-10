class Option:
    def __init__(self, mode: str, cost: float, time: float):
        self.mode = mode
        self.cost = cost
        self.time = time

    def save(self):
        with open('options.txt', 'a') as f:
            f.write(f"{self.mode}|{self.cost}|{self.time}\n")