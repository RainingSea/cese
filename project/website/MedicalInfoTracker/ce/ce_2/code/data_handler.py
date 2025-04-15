from user import User
from medical_info import MedicalInfo
from appointment import Appointment

class DataHandler:
    def save_user(self, user: User) -> None:
        user.save()

    def load_users(self) -> list:
        return User.load_users()

    def save_medical_info(self, info: MedicalInfo) -> None:
        with open('medical_info.txt', 'w') as file:
            for diagnosis in info.diagnoses:
                file.write(f"diagnosis|{diagnosis}\n")
            for medication in info.medications:
                file.write(f"medication|{medication}\n")
            for treatment in info.treatments:
                file.write(f"treatment|{treatment}\n")

    def load_medical_info(self) -> MedicalInfo:
        medical_info = MedicalInfo()
        try:
            with open('medical_info.txt', 'r') as file:
                for line in file:
                    type_, value = line.strip().split('|')
                    if type_ == "diagnosis":
                        medical_info.add_diagnosis(value)
                    elif type_ == "medication":
                        medical_info.add_medication(value)
                    elif type_ == "treatment":
                        medical_info.add_treatment(value)
        except FileNotFoundError:
            pass
        return medical_info

    def save_appointments(self, appointments: Appointment) -> None:
        with open('appointments.txt', 'w') as file:
            for appointment in appointments.appointments:
                file.write(f"{appointment['date']}|{appointment['time']}|{appointment['description']}\n")

    def load_appointments(self) -> Appointment:
        appointments = Appointment()
        try:
            with open('appointments.txt', 'r') as file:
                for line in file:
                    date, time, description = line.strip().split('|')
                    appointments.add_appointment(date, time, description)
        except FileNotFoundError:
            pass
        return appointments