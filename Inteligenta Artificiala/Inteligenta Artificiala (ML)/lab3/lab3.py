#!/usr/bin/env python
# coding: utf-8

# In[28]:


import numpy as np
import matplotlib.pyplot as plt
from sklearn.naive_bayes import MultinomialNB

# In[29]:


train_images = np.loadtxt("data/train_images.txt")
train_labels = np.loadtxt("data/train_labels.txt", 'int')
test_images = np.loadtxt('data/test_images.txt')
test_labels = np.loadtxt('data/test_labels.txt', 'int')


# In[30]:


class KnnClassifier:
    def __init__(self, train_images, train_labels):
        self.train_images = train_images
        self.train_labels = train_labels

    def classify_image(self, test_image, num_neighbors=3, metric='l2'):
        if metric == 'l1':
            distances = np.sum(abs(self.train_images - test_image), axis=1)
        if metric == 'l2':
            distances = np.sqrt(np.sum((self.train_images - test_image) ** 2, axis=1))

        nearestK = np.argsort(distances)[:num_neighbors]
        nearestLabels = self.train_labels[nearestK]
        prediction = np.argmax(np.bincount(nearestLabels))

        return prediction


# In[40]:


# 3
def accuracy(ypred, y_true):
    return np.mean(ypred == y_true)


ob = KnnClassifier(train_images, train_labels)
predictions = []
for imagine in test_images:
    predictions.append(ob.classify_image(imagine, 3, 'l2'))
preds = np.array(predictions)
np.savetxt('predictii_3nn_l2_mnist.txt', preds)

ac = accuracy(preds, test_labels)
print(ac)

# In[38]:


# 4 a
neighbor_num = [1, 3, 5, 7, 9]
acc_arr = []
new_ob = KnnClassifier(train_images, train_labels)
for nums in neighbor_num:
    predictions = np.array([new_ob.classify_image(imagine, nums, 'l2') for imagine in test_images])
    accuracy = np.mean(predictions == test_labels)
    acc_arr.append(accuracy)

np.savetxt('acuratetel2.txt', acc_arr)
plt.plot(neighbor_num, np.array(acc_arr))

# 4 b
acc_arr2 = []
new_ob = KnnClassifier(train_images, train_labels)
for nums in neighbor_num:
    predictions = np.array([new_ob.classify_image(imagine, nums, 'l1') for imagine in test_images])
    accuracy = np.mean(predictions == test_labels)
    acc_arr2.append(accuracy)

np.savetxt('acuratetel1.txt', acc_arr2)
plt.plot(neighbor_num, np.array(acc_arr2))
plt.xlabel('number of neighbors')
plt.ylabel('accuracy')
plt.show()

# In[ ]:




