[OUTPUT]
## general overview of the project
The purpose of this project is to develop a code repository that implements the TextCNN model for movie review sentiment classification using the PyTorch library. This repository should include all the necessary components and features to support the development of the model.

## software functional requirements
1. **Modeling:**
   - The system shall provide the ability to define and manage model-related settings such as kernel sizes, dimension of embedding, and maximum length of sequence.
   - The system shall provide the ability to configure model training settings such as learning rate, batch size, and number of epochs.
   - The system shall provide the ability to define custom parameters during training, such as the number of epochs to save the model and the number of batches to log training loss.
   - The system shall provide the ability to save the model checkpoint with the highest evaluation accuracy during training.
   - The system shall provide the ability to reproduce training and testing results when random seeds are fixed.
   - The system shall provide the ability to log training loss and accuracy for every k batches.
   - The system shall provide the ability to log loss and accuracy for both train and validation sets for each epoch.
   - The system shall provide the ability to calculate the accuracy of model output on the test dataset.
   - The system shall provide the ability to construct the TextCNN model using PyTorch, consisting of an embedding layer, a series of convolutional layers, a maximum pooling layer, ReLU activation function, and a fully connected layer in a fixed order.

2. **Data:**
   - The system shall provide the ability to load and pre-process the IMDb dataset from HuggingFace datasets.
   - The system shall provide the ability to load the `bert-base-uncased` tokenizer from HuggingFace transformers to convert text into vectors.
   - The system shall provide the ability to split the train dataset into train and validation sets, specifying the split ratio to 0.1.

3. **Examples:**
   - The system shall provide example scripts to run the code for both training and testing.
[/OUTPUT]