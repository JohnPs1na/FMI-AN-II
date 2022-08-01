#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
from sklearn.naive_bayes import MultinomialNB

# In[26]:


train_images = np.loadtxt("data/train_images.txt")
train_labels = np.loadtxt("data/train_labels.txt", 'int')
test_images = np.loadtxt('data/test_images.txt')
test_labels = np.loadtxt('data/test_labels.txt', 'int')

image1 = train_images[0, :]
image1 = np.reshape(image1, (28, 28))

plt.imshow(image1.astype(np.uint8), cmap='gray')
plt.show()

bins = np.linspace(start=0, stop=255, num=5)  # returneaza intervalele
image_to_bins = np.digitize(image1, bins) - 1  #

# print(bins)
# print(image_to_bins)

# 1. Antrenarea Modelului   (fit)
# 2. Prezicerea Etichetelor (predict)


naive_bayes_model = MultinomialNB()
naive_bayes_model.fit(train_images, train_labels)

naive_bayes_model.predict(test_images)

naive_bayes_model.score(test_images, test_labels)

# sa vezi si sa nu mai vezi

# In[56]:


intervale = [3, 5, 7, 9, 11]


def value_to_bins(matrice, interval):
    bins = np.linspace(0, 255, interval)
    mat_to_bins = np.digitize(matrice, bins) - 1

    return mat_to_bins


train_images = np.loadtxt("data/train_images.txt")
train_labels = np.loadtxt("data/train_labels.txt", 'int')
test_images = np.loadtxt('data/test_images.txt')
test_labels = np.loadtxt('data/test_labels.txt', 'int')

accuracies = []
for interval in intervale:
    x = value_to_bins(train_images, interval)

    naive_bayes_model = MultinomialNB()

    naive_bayes_model.fit(x, train_labels)

    accuracies.append(naive_bayes_model.score(test_images, test_labels))

best_acc = accuracies[0]
best_acc_idx = 0

for idx, acc in enumerate(accuracies):
    if acc > best_acc:
        best_acc = acc
        best_acc_idx = idx

print(best_acc)
print(best_acc_idx)

interval = intervale[best_acc_idx]

x = value_to_bins(train_images, interval)

naive_bayes_model = MultinomialNB()

naive_bayes_model.fit(x, train_labels)

predicted_labels = naive_bayes_model.predict(test_images)

naive_bayes_model.score(test_images, test_labels)

misclasate = np.where(test_labels != predicted_labels)[0]


# for i in misclasate[:10]:
#     image1 = train_images[i,:]
#     image1 = np.reshape(image1,(28,28))
#     plt.imshow(image1.astype(np.uint8),cmap = 'gray')
#     plt.show()


def confusion_matrix(y_true, y_pred):
    confusion = [[0 for i in range(10)] for j in range(10)]

    for i in range(len(y_true)):
        confusion[y_true[i]][y_pred[i]] += 1

    return confusion


conf = confusion_matrix(test_labels, predicted_labels)

# for i in conf:
#     print(i)


# In[23]:


xs = [(160, 'F'), (165, 'F'), (155, 'F'), (172, 'F'), (175, 'B'), (180, 'B'), (177, 'B'), (190, 'B')]
bins = np.linspace(150, 190, 5)

b = [i[0] for i in xs if i[1] == 'B']
f = [i[0] for i in xs if i[1] == 'F']
b = np.digitize(b, bins)
f = np.digitize(f, bins)

inal = 178
idx = 0
for i in bins:
    if bins[idx] < inal:
        idx += 1

totali = 0
nb = 0
nf = 0
for i in b:
    if i == idx:
        totali += 1
        nb += 1
for i in f:
    if i == idx:
        totali += 1
        nf += 1

print('prob fata = ', nf / totali)
print('prob baiat = ', nb / totali)

# In[ ]:




