import csv

class DataHandler:
    def import_data(self, file_path: str) -> list:
        data = []
        try:
            with open(file_path, mode='r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    data.append(row)
            return data
        except Exception as e:
            print(f"Error importing data: {e}")
            return []
    
    def save_data(self, file_path: str, data: list) -> None:
        try:
            with open(file_path, mode='w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(data)
        except Exception as e:
            print(f"Error saving data: {e}")