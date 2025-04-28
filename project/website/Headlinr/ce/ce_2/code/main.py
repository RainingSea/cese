import nltk
import spacy
from typing import List

class Main:
    def __init__(self):
        self.user_profile_manager = UserProfileManager()
        self.news_manager = NewsManager()

    def main(self) -> str:
        self.user_profile_manager.load_profiles()
        self.news_manager.load_data()
        # Placeholder for user interaction logic
        return "Application started."

class UserProfileManager:
    def __init__(self):
        self.profiles = []

    def create_profile(self, name: str, preferences: List) -> None:
        self.profiles.append({"name": name, "preferences": preferences})
        self.save_profiles()

    def load_profiles(self) -> None:
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    name, preferences = line.strip().split('|')
                    self.profiles.append({"name": name, "preferences": preferences.split(',')})
        except FileNotFoundError:
            print("No profiles found. Starting fresh.")

    def save_profiles(self) -> None:
        with open('users.txt', 'w') as file:
            for profile in self.profiles:
                preferences = ','.join(profile['preferences'])
                file.write(f"{profile['name']}|{preferences}\n")

class NewsManager:
    def __init__(self):
        self.articles = []
        self.summaries = []
        self.bookmarks = []

    def fetch_articles(self) -> None:
        try:
            with open('articles.txt', 'r') as file:
                self.articles = [line.strip() for line in file]
        except FileNotFoundError:
            print("No articles found. Please add articles.")

    def generate_summary(self, article: str) -> str:
        # Simple summary generation logic (placeholder)
        return article[:50] + '...'

    def rank_articles(self, preferences: List) -> List:
        # Placeholder for ranking logic based on user preferences
        return self.articles

    def bookmark_article(self, article: str) -> None:
        self.bookmarks.append(article)
        self.save_data()

    def load_data(self) -> None:
        self.fetch_articles()
        try:
            with open('summaries.txt', 'r') as file:
                self.summaries = [line.strip() for line in file]
            with open('bookmarks.txt', 'r') as file:
                self.bookmarks = [line.strip() for line in file]
        except FileNotFoundError:
            print("No summaries or bookmarks found. Starting fresh.")

    def save_data(self) -> None:
        with open('summaries.txt', 'w') as file:
            for summary in self.summaries:
                file.write(f"{summary}\n")
        with open('bookmarks.txt', 'w') as file:
            for bookmark in self.bookmarks:
                file.write(f"{bookmark}\n")