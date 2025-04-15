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

    def view_info(self) -> dict:
        return {
            "diagnoses": self.diagnoses,
            "medications": self.medications,
            "treatments": self.treatments
        }

    def edit_info(self, diagnosis: str, medication: str, treatment: str) -> None:
        # This function can be expanded to edit existing entries
        pass