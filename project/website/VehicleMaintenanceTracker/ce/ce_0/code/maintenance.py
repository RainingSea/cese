class Maintenance:
    def __init__(self, task: str, date: str, vehicle_id: int):
        self.task = task
        self.date = date
        self.vehicle_id = vehicle_id

    def save(self):
        with open('maintenance.txt', 'a') as f:
            f.write(f"{self.task}|{self.date}|{self.vehicle_id}\n")

    @staticmethod
    def load_maintenance() -> list:
        try:
            with open('maintenance.txt', 'r') as f:
                return [Maintenance(*line.strip().split('|')) for line in f.readlines()]
        except FileNotFoundError:
            return []