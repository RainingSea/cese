class Vehicle:
    def __init__(self, make: str, model: str, year: int, mileage: int):
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.maintenance_records = []

    def add_maintenance(self, task: str, date: str):
        self.maintenance_records.append((task, date))

    def get_maintenance_history(self):
        return self.maintenance_records

    def save(self):
        with open('vehicles.txt', 'a') as file:
            records_str = ';'.join([f'{task},{date}' for task, date in self.maintenance_records])
            file.write(f'{self.make}|{self.model}|{self.year}|{self.mileage}|{records_str}\n')

    @staticmethod
    def load_all():
        vehicles = []
        try:
            with open('vehicles.txt', 'r') as file:
                for line in file:
                    make, model, year, mileage, records = line.strip().split('|')
                    vehicle = Vehicle(make, model, int(year), int(mileage))
                    if records:
                        records_list = records.split(';')
                        for record in records_list:
                            task, date = record.split(',')
                            vehicle.add_maintenance(task, date)
                    vehicles.append(vehicle)
        except FileNotFoundError:
            pass
        return vehicles