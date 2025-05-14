import json

class PreferenceManager:
    def __init__(self, prefs_file):
        self.prefs_file = prefs_file

    def save_preferences(self, username, budget, activities, climate):
        with open(self.prefs_file, 'a') as f:
            activities_str = ','.join(activities)
            f.write(f"{username}|{budget}|{activities_str}|{climate}\n")
        return True

    def get_preferences(self, username):
        with open(self.prefs_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == username:
                    return {
                        'budget': int(parts[1]),
                        'activities': parts[2].split(','),
                        'climate': parts[3]
                    }
        return None

class DestinationManager:
    def __init__(self, dest_file, fav_file):
        self.dest_file = dest_file
        self.fav_file = fav_file

    def get_recommendations(self, prefs):
        recommendations = []
        with open(self.dest_file, 'r') as f:
            for line in f:
                dest = json.loads(line)
                if (dest['climate'] == prefs['climate'] and 
                    any(activity in dest['activities'] for activity in prefs['activities']) and
                    dest['cost'] <= prefs['budget']):
                    recommendations.append(dest)
        return recommendations

    def save_favorite(self, username, destination):
        with open(self.fav_file, 'a') as f:
            f.write(f"{username}|{destination}\n")
        return True