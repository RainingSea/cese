from datetime import datetime
import os
from flask import flash

class TutorHandler:
    def __init__(self, tutors_file, requests_file):
        self.tutors_file = tutors_file
        self.requests_file = requests_file
        self._ensure_files_exist()
    
    def get_all_tutors(self):
        tutors = self._read_tutors_file()
        return [{
            'id': tutor.split('|')[0],
            'name': tutor.split('|')[1],
            'subjects': tutor.split('|')[2].split(',')
        } for tutor in tutors]
    
    def add_request(self, student, tutor_id, subject, details, date):
        try:
            datetime.strptime(date, '%Y-%m-%d')
            requests = self._read_requests_file()
            request_id = f"req_{len(requests)+1}"
            requests.append(f"{request_id}|{student}|{tutor_id}|{subject}|{details}|{date}|pending")
            return self._write_requests_file(requests)
        except ValueError:
            return False
    
    def get_requests(self, username):
        requests = self._read_requests_file()
        user_requests = []
        for req in requests:
            parts = req.split('|')
            if parts[1] == username or parts[2] == username:
                user_requests.append({
                    'id': parts[0],
                    'student': parts[1],
                    'tutor': parts[2],
                    'subject': parts[3],
                    'details': parts[4],
                    'date': parts[5],
                    'status': parts[6]
                })
        return user_requests
    
    def cancel_request(self, username, request_id):
        requests = self._read_requests_file()
        updated_requests = []
        cancelled = False
        
        for req in requests:
            parts = req.split('|')
            if parts[0] == request_id and parts[1] == username and parts[6] == 'pending':
                cancelled = True
            else:
                updated_requests.append(req)
        
        if cancelled:
            return self._write_requests_file(updated_requests)
        return False
    
    def _ensure_files_exist(self):
        for file_path in [self.tutors_file, self.requests_file]:
            if not os.path.exists(file_path):
                open(file_path, 'a').close()
    
    def _read_tutors_file(self):
        try:
            with open(self.tutors_file, 'r') as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            return []
    
    def _read_requests_file(self):
        try:
            with open(self.requests_file, 'r') as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            return []
    
    def _write_requests_file(self, requests):
        try:
            with open(self.requests_file, 'w') as f:
                f.write('\n'.join(requests))
            return True
        except Exception as e:
            flash('Error saving request data')
            return False