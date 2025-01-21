import nltk

class NewsSummaryGenerator:
    def __init__(self):
        nltk.download('punkt')

    def generate_summary(self, article: str, preferences: dict) -> str:
        sentences = nltk.sent_tokenize(article)
        summary = ' '.join(sentences[:2])  # Simple summary: first two sentences
        return summary