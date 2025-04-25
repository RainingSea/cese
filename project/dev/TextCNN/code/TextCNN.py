import torch
import torch.nn as nn
import torch.optim as optim

class TextCNN(nn.Module):
    def __init__(self, vocab_size, embedding_dim, num_classes):
        super(TextCNN, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.conv_layers = nn.ModuleList([
            nn.Conv2d(1, 100, (kernel_size, embedding_dim)) for kernel_size in [3, 4, 5]
        ])
        self.max_pool = nn.AdaptiveMaxPool1d(1)
        self.fc = nn.Linear(300, num_classes)  # 100 filters * 3 kernel sizes

    def forward(self, input: torch.Tensor) -> torch.Tensor:
        embedded = self.embedding(input).unsqueeze(1)  # Add channel dimension
        conv_results = [conv(embedded) for conv in self.conv_layers]
        pooled_results = [self.max_pool(result.squeeze(3)).squeeze(2) for result in conv_results]
        concatenated = torch.cat(pooled_results, dim=1)
        return self.fc(concatenated)

    def train_model(self, train_loader, criterion, optimizer, num_epochs):
        for epoch in range(num_epochs):
            for inputs, labels in train_loader:
                optimizer.zero_grad()
                outputs = self.forward(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

    def evaluate(self, test_loader) -> float:
        total, correct = 0, 0
        with torch.no_grad():
            for inputs, labels in test_loader:
                outputs = self.forward(inputs)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        return correct / total