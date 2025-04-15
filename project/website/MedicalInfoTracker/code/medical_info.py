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

    def view_history(self) -> dict:
        return {
            'diagnoses': self.diagnoses,
            'medications': self.medications,
            'treatments': self.treatments
        }

    def edit_entry(self, entry_type: str, old_value: str, new_value: str) -> None:
        if entry_type == 'diagnosis':
            self.diagnoses = [new_value if d == old_value else d for d in self.diagnoses]
        elif entry_type == 'medication':
            self.medications = [new_value if m == old_value else m for m in self.medications]
        elif entry_type == 'treatment':
            self.treatments = [new_value if t == old_value else t for t in self.treatments]