from werkzeug.security import generate_password_hash, check_password_hash

class TravelTipper:
    def __init__(self, user_file='users.txt', tips_file='tips.txt', favorites_file='favorites.txt'):
        self.user_file = user_file
        self.tips_file = tips_file
        self.favorites_file = favorites_file

    def register_user(self, username, password):
        with open(self.user_file, 'a+') as f:
            f.seek(0)
            for line in f:
                if line.split(':')[0] == username:
                    return False
            f.write(f"{username}:{password}\n")
        return True

    def login_user(self, username, password):
        with open(self.user_file, 'r') as f:
            for line in f:
                stored_username, stored_password = line.strip().split(':')
                if stored_username == username and stored_password == password:
                    return True
        return False

    def get_tips(self, destination, interests):
        tips = []
        with open(self.tips_file, 'r') as f:
            for line in f:
                tip_dest, category, content = line.strip().split('|')
                if tip_dest.lower() == destination.lower() and category.lower() in [i.lower() for i in interests]:
                    tips.append({'id': hash(line), 'destination': tip_dest, 'category': category, 'content': content})
        return tips

    def save_favorite(self, username, tip_id):
        with open(self.favorites_file, 'a') as f:
            f.write(f"{username}|{tip_id}\n")
        return True

    def get_favorites(self, username):
        favorites = []
        with open(self.favorites_file, 'r') as f:
            for line in f:
                user, tip_id = line.strip().split('|')
                if user == username:
                    favorites.append(tip_id)
        return favorites