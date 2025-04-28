class MedicalInfoManager:
    def __init__(self):
        self.medical_info = self.load_medical_info()

    def load_medical_info(self):
        medical_info = []
        try:
            with open('medical_info.txt', 'r') as file:
                for line in file:
                    medical_info.append(line.strip())
        except FileNotFoundError:
            pass
        return medical_info

    def add_diagnosis(self, diagnosis: str):
        self.medical_info.append(f"Diagnosis: {diagnosis}")
        self.save_medical_info()

    def add_medication(self, medication: str):
        self.medical_info.append(f"Medication: {medication}")
        self.save_medical_info()

    def add_treatment(self, treatment: str):
        self.medical_info.append(f"Treatment: {treatment}")
        self.save_medical_info()

    def view_medical_info(self):
        return self.medical_info

    def save_medical_info(self):
        with open('medical_info.txt', 'w') as file:
            for info in self.medical_info:
                file.write(f"{info}\n")