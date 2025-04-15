from user import User
from medical_info import MedicalInfo
from appointment import Appointment

class DataHandler:
    def login(self, username: str, password: str) -> bool:
        users = User.load_users()
        for user in users:
            if user.username == username and user.password == password:
                return True
        return False

    def save_user(self, user: User) -> None:
        user.save()

    def load_users(self) -> list:
        return User.load_users()

    def save_medical_info(self, info: MedicalInfo) -> None:
        info.save()

    def load_medical_info(self) -> MedicalInfo:
        return MedicalInfo.load()

    def save_appointments(self, appointments: Appointment) -> None:
        appointments.save()

    def load_appointments(self) -> Appointment:
        return Appointment.load()