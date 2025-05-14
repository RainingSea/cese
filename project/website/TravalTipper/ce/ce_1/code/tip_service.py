class TipService:
    def __init__(self, tips_file='tips_database.txt', saved_tips_file='saved_tips.txt'):
        self.tips_file = tips_file
        self.saved_tips_file = saved_tips_file

    def get_tips(self, destination, interests):
        tips = []
        with open(self.tips_file, 'r') as file:
            for line in file:
                tip_dest, category, tip_text = line.strip().split('|')
                if tip_dest.lower() == destination.lower() and category in interests:
                    tips.append({'id': f"{tip_dest.lower()}_{category}", 'text': tip_text})
        return tips

    def save_tip(self, username, tip_id):
        with open(self.saved_tips_file, 'a') as file:
            file.write(f"{username}|{tip_id}\n")
        return True

    def get_saved_tips(self, username):
        saved_tips = []
        with open(self.saved_tips_file, 'r') as file:
            for line in file:
                user, tip_id = line.strip().split('|')
                if user == username:
                    saved_tips.append(tip_id)
        return saved_tips