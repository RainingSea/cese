import csv

class DataLoader:
    def load_data(self, file_path: str) -> list:
        data = []
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
        return data