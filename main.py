import torch
import time
import torch.nn as nn
import matplotlib.pyplot as plt
from model import convnet
from font_dataset import FontDataset

start = time.time()
b_size = 1

torch.manual_seed(7777)
torch.cuda.manual_seed(7777)

train_dir = './npy_train'
val_dir = './npy_val'
train_dataset = FontDataset(train_dir)
val_dataset = FontDataset(val_dir)
train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                           batch_size = b_size, shuffle=True)

val_loader = torch.utils.data.DataLoader(dataset=val_dataset,
                                         batch_size = 1)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = convnet().to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, weight_decay = 1e-5)

num_epochs = 2
losses = []
for epoch in range(num_epochs):
    for i, (images, labels) in enumerate(train_loader):
        # Assign Tensors to Configured Device
        images = images.to(device) # reshape dimensions of the input images to fit model
        labels = labels.to(device)

        # Forward Propagation
        outputs = model(images)

        # Get Loss, Compute Gradient, Update Parameters
        loss = criterion(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if i%50 == 0:
            print(f"Epoch : {epoch+1} | loss for {i*b_size} : {loss}")
        
        

end = time.time()
duration = end - start
print("걸린 시간 : {}m{}s".format(int(duration//60), int(duration%60)))

# Test after Training is done
with torch.no_grad():
    correct = 0
    total = 0
    for i, (images, labels) in enumerate(val_loader):
        images = images.to(device) # reshape dimensions of the input images to fit model
        labels = labels.to(device)
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    print("acc : {} %" .format(correct / 5000))


