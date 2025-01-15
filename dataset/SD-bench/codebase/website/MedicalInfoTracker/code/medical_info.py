class MedicalInfo:
    def __init__(self, diagnoses: list, medications: list, treatments: list):
        self.diagnoses = diagnoses
        self.medications = medications
        self.treatments = treatments

    def add_diagnosis(self, diagnosis: str):
        self.diagnoses.append(diagnosis)

    def remove_diagnosis(self, diagnosis: str):
        self.diagnoses.remove(diagnosis)

    def update_medication(self, medication: str):
        if medication not in self.medications:
            self.medications.append(medication)

    def get_medical_info(self) -> dict:
        return {
            'diagnoses': self.diagnoses,
            'medications': self.medications,
            'treatments': self.treatments
        }

    def save(self):
        with open('medical_info.txt', 'a') as file:
            file.write(f"{','.join(self.diagnoses)}|{','.join(self.medications)}|{','.join(self.treatments)}\n")