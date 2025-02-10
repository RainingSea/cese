class TravelTip:
    def __init__(self, destination: str, duration: str, interests: list):
        self.destination = destination
        self.duration = duration
        self.interests = interests
        self.tips = self.load_tips()

    def generate_tips(self) -> dict:
        recommendations = []
        for tip in self.tips.get(self.destination, []):
            if any(interest in tip['interests'] for interest in self.interests):
                recommendations.append(tip['tip'])
        return {'destination': self.destination, 'recommendations': recommendations}

    @staticmethod
    def load_tips() -> dict:
        tips = {}
        with open('tips.txt', 'r') as file:
            for line in file:
                destination, duration, interests, tip = line.strip().split('|')
                if destination not in tips:
                    tips[destination] = []
                tips[destination].append({'duration': duration, 'interests': interests.split(','), 'tip': tip})
        return tips