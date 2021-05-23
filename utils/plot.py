# This program is basically used to show 
#  both validation and training loss in one plot by using train.log file
# but first you have to perform cat train.log | grep "train loss" > output.txt
# then run this program to get the plot
import matplotlib.pyplot as plt
import re
val_loss = []
train_loss = []
epochs = range(1,131)
with open("/home/emekonnen/mydata/E2E-ASR/libri_exp3/ctc_bi_lr1e-3/output.txt", "r") as f:
    count = 1
    for line in f:
        line = line.split()
        train_loss.append(float(re.sub("[^0-9.]", "",line[8])))
        val_loss.append(float(re.sub("[^0-9.]", "",line[13])))
plt.figure(figsize=(10,5))
plt.title("Training and Validation loss")
plt.plot(epochs, val_loss[:-1], 'y', label = "Validation Loss")
plt.plot(epochs, train_loss[:-1], 'b', label="Training Loss")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.savefig("/home/emekonnen/mydata/loss1.png")
#plt.show()
