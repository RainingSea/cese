import os
import tempfile
from threading import Lock

class TravelTipper:
    def __init__(self, users_file='users.txt', tips_file='tips.txt', favorites_file='favorites.txt'):
        self.users_file = users_file
        self.tips_file = tips_file
        self.favorites_file = favorites_file
        self.lock = Lock()
        
        # Initialize files if they don't exist
        for file in [self.users_file, self.tips_file, self.favorites_file]:
            if not os.path.exists(file):
                with open(file, 'w') as f:
                    pass

    def register_user(self, username, password):
        if not username or not password:
            return "EMPTY_FIELDS"
            
        with self.lock:
            users = self._read_file(self.users_file)
            for user in users:
                if user.split('|')[0] == username:
                    return "USER_EXISTS"
                    
            if self._write_file(self.users_file, f"{username}|{password}\n", 'a'):
                return "SUCCESS"
            return "WRITE_ERROR"

    def login_user(self, username, password):
        users = self._read_file(self.users_file)
        for user in users:
            parts = user.strip().split('|')
            if len(parts) == 2 and parts[0] == username and parts[1] == password:
                return True
        return False

    def get_tips(self, destination, interests):
        tips = self._read_file(self.tips_file)
        filtered_tips = []
        
        for tip in tips:
            parts = tip.strip().split('|')
            if len(parts) >= 4 and parts[1].lower() == destination.lower():
                if not interests or parts[2].lower() in [i.lower() for i in interests]:
                    filtered_tips.append({
                        'id': f"{parts[1]}_{parts[2]}",
                        'destination': parts[1],
                        'category': parts[2],
                        'content': parts[3]
                    })
                
        return filtered_tips

    def search_tips(self, query):
        if not query:
            return []
            
        tips = self._read_file(self.tips_file)
        results = []
        
        for tip in tips:
            parts = tip.strip().split('|')
            if len(parts) >= 4 and query.lower() in '|'.join(parts[1:]).lower():
                results.append({
                    'id': f"{parts[1]}_{parts[2]}",
                    'destination': parts[1],
                    'category': parts[2],
                    'content': parts[3]
                })
                
        return results

    def save_favorite(self, username, tip_id):
        with self.lock:
            favorites = self._read_file(self.favorites_file)
            for fav in favorites:
                parts = fav.strip().split('|')
                if len(parts) == 2 and parts[0] == username and parts[1] == tip_id:
                    return "ALREADY_FAVORITED"
                    
            if self._write_file(self.favorites_file, f"{username}|{tip_id}\n", 'a'):
                return "SUCCESS"
            return "WRITE_ERROR"

    def get_favorites(self, username):
        favorites = self._read_file(self.favorites_file)
        tips = self._read_file(self.tips_file)
        user_favorites = []
        
        fav_tip_ids = []
        for fav in favorites:
            parts = fav.strip().split('|')
            if len(parts) == 2 and parts[0] == username:
                fav_tip_ids.append(parts[1])
        
        for tip in tips:
            parts = tip.strip().split('|')
            if len(parts) >= 4 and f"{parts[1]}_{parts[2]}" in fav_tip_ids:
                user_favorites.append({
                    'id': f"{parts[1]}_{parts[2]}",
                    'destination': parts[1],
                    'category': parts[2],
                    'content': parts[3]
                })
                
        return user_favorites

    def _read_file(self, filename):
        try:
            with open(filename, 'r') as f:
                return f.readlines()
        except:
            return []

    def _write_file(self, filename, content, mode='w'):
        try:
            temp = tempfile.NamedTemporaryFile(mode=mode, delete=False)
            with temp:
                if mode == 'a' and os.path.exists(filename):
                    with open(filename, 'r') as f:
                        temp.write(f.read())
                temp.write(content)
            
            os.replace(temp.name, filename)
            return True
        except:
            return False