class RecommendationEngine:
    def __init__(self, dest_file='destinations.txt'):
        self.dest_file = dest_file

    def _load_destinations(self):
        destinations = []
        try:
            with open(self.dest_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 7:
                        destinations.append({
                            'id': parts[0],
                            'name': parts[1],
                            'activities': parts[2].split(','),
                            'climate': parts[3],
                            'min_budget': int(parts[4]),
                            'max_budget': int(parts[5]),
                            'description': parts[6]
                        })
        except IOError:
            pass
        return destinations

    def get_recommendations(self, prefs):
        destinations = self._load_destinations()
        if not prefs:
            return destinations
            
        budget = prefs.get('budget', 0)
        activities = prefs.get('activities', [])
        climate = prefs.get('climate', '')
        
        filtered = []
        for dest in destinations:
            if (dest['min_budget'] <= budget <= dest['max_budget'] and
                (not climate or dest['climate'] == climate) and
                (not activities or any(act in dest['activities'] for act in activities))):
                filtered.append(dest)
        return filtered

    def get_destination(self, dest_id):
        destinations = self._load_destinations()
        for dest in destinations:
            if dest['id'] == dest_id:
                return dest
        return None