from transformers import BertTokenizer

class Tokenizer:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    def tokenize(self, text: str) -> list[int]:
        return self.tokenizer.encode(text, add_special_tokens=True)