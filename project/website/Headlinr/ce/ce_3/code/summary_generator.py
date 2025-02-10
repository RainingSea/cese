from transformers import pipeline

class SummaryGenerator:
    def __init__(self):
        self.summarizer = pipeline("summarization")

    def generate_summary(self, article: str) -> str:
        summary = self.summarizer(article, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']