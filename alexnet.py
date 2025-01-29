# -*- coding: utf-8 -*-
"""alexnet.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1itm3ScMGXg2zPbguPbXJi5q9FTtrR5jA
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
import matplotlib.pyplot as plt

batch_size = 32
learning_rate = 0.001
num_epochs = 5
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

device

transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=3),
    transforms.Resize((224, 224)),  # Resize images to 224x224
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalization for AlexNet
])

train_dataset = datasets.FashionMNIST(root='./data', train=True, download=True, transform=transform)
test_dataset = datasets.FashionMNIST(root='./data', train=False, download=True, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

alexnet = models.alexnet(pretrained=True)
for param in alexnet.parameters():
    param.requires_grad = False

alexnet.classifier[6] = nn.Linear(in_features=4096, out_features=10)
alexnet.to(device)

loss_fn = nn.CrossEntropyLoss()
optimizer = optim.Adam(alexnet.classifier[6].parameters(), lr = learning_rate)

# Training loop
for epoch in range(num_epochs):
    alexnet.train()  # Set model to training mode
    running_loss = 0.0
    correct = 0
    total = 0

    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)

        # Zero the parameter gradients
        optimizer.zero_grad()

        # Forward pass
        outputs = alexnet(inputs)

        # Compute the loss
        loss = loss_fn(outputs, labels)

        # Backward pass and optimization
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

        # Calculate accuracy
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    # Calculate average loss and accuracy for this epoch
    epoch_loss = running_loss / len(train_loader)
    epoch_accuracy = (correct / total) * 100

    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss:.4f}, Accuracy: {epoch_accuracy:.2f}%")

alexnet.eval()
correct = 0
total = 0

with torch.no_grad():
    for inputs, labels in test_loader:
        inputs, labels = inputs.to(device), labels.to(device)

        outputs = alexnet(inputs)

        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

test_accuracy = (correct / total) * 100
print(f"Test Accuracy: {test_accuracy:.2f}%")

alexnet.eval()
dataiter = iter(test_loader)
images, labels = next(dataiter)

images, labels = images.to(device), labels.to(device)

outputs = alexnet(images)
_, predicted = torch.max(outputs, 1)

fig = plt.figure(figsize=(10, 5))
for i in range(6):
    ax = fig.add_subplot(2, 3, i+1)
    ax.imshow(images[i].cpu().numpy().transpose(1, 2, 0))
    ax.set_title(f"Pred: {predicted[i].item()}, True: {labels[i].item()}")
plt.show()

alexnet.eval()
dataiter = iter(test_loader)

images, labels = next(dataiter)

images, labels = images.to(device), labels.to(device)

outputs = alexnet(images)
_, predicted = torch.max(outputs, 1)

fig = plt.figure(figsize=(12, 12))
for i in range(12):
    ax = fig.add_subplot(3, 4, i+1)
    ax.imshow(images[i].cpu().numpy().transpose(1, 2, 0))
    ax.set_title(f"Pred: {predicted[i].item()}, True: {labels[i].item()}")
plt.tight_layout()
plt.show()

import seaborn as sns
from sklearn.metrics import confusion_matrix

alexnet.eval()

all_predictions = []
all_labels = []

with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)

        outputs = alexnet(images)

        _, predicted = torch.max(outputs, 1)

        all_labels.extend(labels.cpu().numpy())
        all_predictions.extend(predicted.cpu().numpy())

cm = confusion_matrix(all_labels, all_predictions)

plt.figure(figsize=(10, 7))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=[f"Class {i}" for i in range(10)], yticklabels=[f"Class {i}" for i in range(10)], cbar=False)
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()

