from werkzeug.security import generate_password_hash, check_password_hash

class DataHandler:
    def __init__(self):
        self.users_file = 'users.txt'
        self.notes_prefix = 'notes_'
    
    def register_user(self, username, password):
        with open(self.users_file, 'a+') as f:
            f.seek(0)
            for line in f:
                if line.startswith(username + '|'):
                    return False
            f.write(f"{username}|{password}\n")
        return True
    
    def authenticate_user(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                stored_username, stored_password = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False
    
    def get_notes(self, username):
        notes = []
        try:
            with open(f"{self.notes_prefix}{username}.txt", 'r') as f:
                for line in f:
                    note_id, title, content, timestamp = line.strip().split('|')
                    notes.append({
                        'id': note_id,
                        'title': title,
                        'content': content,
                        'timestamp': timestamp
                    })
        except FileNotFoundError:
            pass
        return notes
    
    def add_note(self, username, title, content):
        notes = self.get_notes(username)
        new_id = str(len(notes) + 1)
        with open(f"{self.notes_prefix}{username}.txt", 'a') as f:
            f.write(f"{new_id}|{title}|{content}|2023-11-20\n")
        return True
    
    def update_note(self, username, note_id, title, content):
        notes = self.get_notes(username)
        updated = False
        with open(f"{self.notes_prefix}{username}.txt", 'w') as f:
            for note in notes:
                if note['id'] == note_id:
                    f.write(f"{note_id}|{title}|{content}|2023-11-20\n")
                    updated = True
                else:
                    f.write(f"{note['id']}|{note['title']}|{note['content']}|{note['timestamp']}\n")
        return updated
    
    def delete_note(self, username, note_id):
        notes = self.get_notes(username)
        deleted = False
        with open(f"{self.notes_prefix}{username}.txt", 'w') as f:
            for note in notes:
                if note['id'] != note_id:
                    f.write(f"{note['id']}|{note['title']}|{note['content']}|{note['timestamp']}\n")
                else:
                    deleted = True
        return deleted
    
    def search_notes(self, username, query):
        notes = self.get_notes(username)
        results = []
        for note in notes:
            if query.lower() in note['title'].lower() or query.lower() in note['content'].lower():
                results.append(note)
        return results