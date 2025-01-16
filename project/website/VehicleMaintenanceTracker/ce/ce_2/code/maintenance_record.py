class MaintenanceRecord:
    def __init__(self, vehicle_id: int, task: str, date: str):
        self.vehicle_id = vehicle_id
        self.task = task
        self.date = date

    def save(self):
        with open('maintenance.txt', 'a') as file:
            file.write(f"{self.vehicle_id}|{self.task}|{self.date}\n")

    @staticmethod
    def load_all() -> list:
        records = []
        with open('maintenance.txt', 'r') as file:
            for line in file:
                vehicle_id, task, date = line.strip().split('|')
                records.append(MaintenanceRecord(int(vehicle_id), task, date))
        return records