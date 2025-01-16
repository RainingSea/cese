class Maintenance:
    def __init__(self, task: str, date: str, vehicle_id: int):
        self.task = task
        self.date = date
        self.vehicle_id = vehicle_id

    def save(self) -> None:
        with open('maintenance.txt', 'a') as f:
            f.write(f"{self.task}|{self.date}|{self.vehicle_id}\n")

    @staticmethod
    def load_all() -> list:
        maintenance_records = []
        with open('maintenance.txt', 'r') as f:
            for line in f:
                task, date, vehicle_id = line.strip().split('|')
                maintenance_records.append(Maintenance(task, date, int(vehicle_id)))
        return maintenance_records