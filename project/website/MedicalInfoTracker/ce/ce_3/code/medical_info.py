class MedicalInfo:
    def __init__(self):
        self.records = self.load_records()

    def load_records(self):
        records = []
        with open('medical_info.txt', 'r') as file:
            for line in file:
                records.append(line.strip().split('|'))
        return records

    def add_record(self, diagnosis: str, medication: str, treatment: str) -> None:
        record = [diagnosis, medication, treatment]
        self.records.append(record)
        with open('medical_info.txt', 'a') as file:
            file.write('|'.join(record) + '\n')

    def edit_record(self, index: int, diagnosis: str, medication: str, treatment: str) -> None:
        if 0 <= index < len(self.records):
            self.records[index] = [diagnosis, medication, treatment]
            self.save_records()

    def view_records(self) -> list:
        return self.records

    def save_records(self):
        with open('medical_info.txt', 'w') as file:
            for record in self.records:
                file.write('|'.join(record) + '\n')