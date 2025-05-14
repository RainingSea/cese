class TutorHandler:
    def __init__(self, tutors_file, requests_file):
        self.tutors_file = tutors_file
        self.requests_file = requests_file

    def get_all_tutors(self):
        tutors = []
        try:
            with open(self.tutors_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) >= 3:
                        tutors.append({
                            'id': parts[0],
                            'name': parts[1],
                            'subjects': parts[2]
                        })
        except FileNotFoundError:
            pass
        return tutors

    def create_request(self, student, subject, details, date):
        try:
            request_id = len(open(self.requests_file).readlines()) + 1 if open(self.requests_file).readlines() else 1
            with open(self.requests_file, 'a') as f:
                f.write(f"{request_id}|{student}|None|{subject}|{details}|{date}|pending\n")
            return True
        except:
            return False