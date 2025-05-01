class CharitableGivingPlatform:
    def __init__(self, users_file='users.txt', charities_file='charities.txt', donations_file='donations.txt'):
        self.users_file = users_file
        self.charities_file = charities_file
        self.donations_file = donations_file
        self._initialize_data_files()

    def _initialize_data_files(self):
        """Ensure data files exist with initial data if empty"""
        try:
            with open(self.users_file, 'a+') as f:
                pass
            with open(self.charities_file, 'a+') as f:
                if f.tell() == 0:
                    f.write("1|Red Cross|Help people affected by disasters|Disaster Relief,Blood Donation\n")
                    f.write("2|WWF|Conserve nature and reduce threats to diversity|Wildlife Conservation,Habitat Protection\n")
                    f.write("3|UNICEF|Protect children's rights worldwide|Education,Healthcare,Nutrition\n")
            with open(self.donations_file, 'a+') as f:
                pass
        except IOError:
            pass

    def register_user(self, username, password):
        try:
            with open(self.users_file, 'r+') as f:
                for line in f:
                    existing_username, _ = line.strip().split('|')
                    if existing_username == username:
                        return False
                f.write(f"{username}|{password}\n")
            return True
        except Exception:
            return False

    def login_user(self, username, password):
        try:
            with open(self.users_file, 'r') as f:
                for line in f:
                    stored_username, stored_password = line.strip().split('|')
                    if stored_username == username and stored_password == password:
                        return True
            return False
        except Exception:
            return False

    def get_charities(self):
        charities = []
        try:
            with open(self.charities_file, 'r') as f:
                for line in f:
                    charity_id, name, mission, projects = line.strip().split('|')
                    charities.append({
                        'id': charity_id,
                        'name': name,
                        'mission': mission,
                        'projects': projects.split(',')
                    })
        except Exception:
            pass
        return charities

    def get_charity_details(self, charity_id):
        try:
            with open(self.charities_file, 'r') as f:
                for line in f:
                    c_id, name, mission, projects = line.strip().split('|')
                    if c_id == charity_id:
                        return {
                            'id': c_id,
                            'name': name,
                            'mission': mission,
                            'projects': projects.split(',')
                        }
        except Exception:
            pass
        return None

    def make_donation(self, username, charity_id, amount):
        try:
            amount = float(amount)
            if amount <= 0:
                return False

            with open(self.donations_file, 'a') as f:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"{username}|{charity_id}|{amount}|{timestamp}\n")
            return True
        except Exception:
            return False

    def get_user_donations(self, username):
        donations = []
        try:
            with open(self.donations_file, 'r') as f:
                for line in f:
                    donor, charity_id, amount, timestamp = line.strip().split('|')
                    if donor == username:
                        donations.append({
                            'charity_id': charity_id,
                            'amount': float(amount),
                            'timestamp': timestamp
                        })
        except Exception:
            pass
        return donations