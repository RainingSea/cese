import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from Tokenizer import Tokenizer
from Dataset import Dataset
from TextCNN import TextCNN

class Main:
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.dataset = Dataset()
        self.model = None

    def main(self) -> str:
        self.dataset.load_data()
        train_data, val_data = self.dataset.split_data()
        self.model = TextCNN(vocab_size=30522, embedding_dim=300, num_classes=2)  # BERT vocab size
        train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
        val_loader = DataLoader(val_data, batch_size=32, shuffle=False)

        criterion = torch.nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=0.001)

        self.train(train_loader, criterion, optimizer, num_epochs=5)
        accuracy = self.test(val_loader)
        return f"Validation Accuracy: {accuracy:.2f}"

    def train(self, train_loader, criterion, optimizer, num_epochs):
        self.model.train_model(train_loader, criterion, optimizer, num_epochs)

    def test(self, val_loader) -> float:
        return self.model.evaluate(val_loader)

if __name__ == "__main__":
    main_instance = Main()
    print(main_instance.main())