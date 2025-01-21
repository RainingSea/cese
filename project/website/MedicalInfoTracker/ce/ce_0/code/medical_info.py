class MedicalInfo:
    def __init__(self):
        self.diagnoses = []
        self.medications = []
        self.treatments = []

    def add_diagnosis(self, diagnosis: str) -> None:
        self.diagnoses.append(diagnosis)

    def add_medication(self, medication: str) -> None:
        self.medications.append(medication)

    def add_treatment(self, treatment: str) -> None:
        self.treatments.append(treatment)

    def get_medical_info(self) -> dict:
        return {
            'diagnoses': self.diagnoses,
            'medications': self.medications,
            'treatments': self.treatments
        }