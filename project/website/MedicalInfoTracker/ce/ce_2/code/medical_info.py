class MedicalInfo:
    def __init__(self, diagnoses: list, medications: list, treatments: list):
        self.diagnoses = diagnoses
        self.medications = medications
        self.treatments = treatments

    def add_diagnosis(self, diagnosis: str):
        self.diagnoses.append(diagnosis)

    def add_medication(self, medication: str):
        self.medications.append(medication)

    def add_treatment(self, treatment: str):
        self.treatments.append(treatment)

    def save(self):
        with open('medical_info.txt', 'a') as file:
            file.write(f"{','.join(self.diagnoses)}|{','.join(self.medications)}|{','.join(self.treatments)}\n")