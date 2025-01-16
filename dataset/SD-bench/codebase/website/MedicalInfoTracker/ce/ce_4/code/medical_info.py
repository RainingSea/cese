class MedicalInfo:
    def __init__(self, diagnoses: list, medications: list, treatments: list):
        self.diagnoses = diagnoses
        self.medications = medications
        self.treatments = treatments

    def save(self):
        with open('medical_info.txt', 'a') as file:
            file.write(f"{self.username}|{','.join(self.diagnoses)},{','.join(self.medications)},{','.join(self.treatments)}\n")