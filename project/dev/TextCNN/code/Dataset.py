from datasets import load_dataset
from sklearn.model_selection import train_test_split

class Dataset:
    def __init__(self):
        self.data = None

    def load_data(self):
        self.data = load_dataset('imdb')

    def split_data(self):
        train_data, val_data = train_test_split(self.data['train'], test_size=0.1)
        return train_data, val_data