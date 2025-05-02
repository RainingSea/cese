import datetime

class BirthdateManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.birthdates = self.load_birthdates()

    def load_birthdates(self) -> list:
        """Loads birthdates from the 'birthdates.txt' file and returns them as a list."""
        try:
            with open(self.file_path, 'r') as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            return []

    def save_birthdate(self, birthdate: str) -> None:
        """Saves a new birthdate to the 'birthdates.txt' file."""
        with open(self.file_path, 'a') as file:
            file.write(birthdate + '\n')
        self.birthdates.append(birthdate)

    def calculate_age(self, birthdate: str) -> tuple:
        """Calculates the age in years, months, and days based on the inputted birthdate."""
        birth_date = datetime.datetime.strptime(birthdate, '%Y-%m-%d')
        today = datetime.datetime.today()
        age_years = today.year - birth_date.year
        age_months = today.month - birth_date.month
        age_days = today.day - birth_date.day

        if age_days < 0:
            age_months -= 1
            last_month = (today.month - 1) if today.month > 1 else 12
            last_month_year = today.year if last_month != 12 else today.year - 1
            days_in_last_month = (datetime.datetime(last_month_year, last_month + 1, 1) - 
                                   datetime.timedelta(days=1)).day
            age_days += days_in_last_month

        if age_months < 0:
            age_years -= 1
            age_months += 12

        return age_years, age_months, age_days

    def days_until_next_birthday(self, birthdate: str) -> int:
        """Calculates the number of days remaining until the next birthday based on the inputted birthdate."""
        birth_date = datetime.datetime.strptime(birthdate, '%Y-%m-%d')
        today = datetime.datetime.today()
        next_birthday = birth_date.replace(year=today.year)

        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)

        return (next_birthday - today).days

    def validate_birthdate_format(self, birthdate: str) -> bool:
        """Validates the format of the input birthdate and checks if it is a realistic date."""
        try:
            datetime.datetime.strptime(birthdate, '%Y-%m-%d')
            return True
        except ValueError:
            return False