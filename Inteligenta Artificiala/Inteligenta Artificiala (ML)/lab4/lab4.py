#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sklearn import preprocessing  # StandardScaler, MinMaxScaler, Normalizer(norm = 'l?')
from sklearn import svm
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
import numpy as np

# In[8]:


x_train = np.array([[1, -1, 2], [2, 0, 0], [0, 1, -1]], dtype=np.float64)
x_test = np.array([[-1, 1, 0]], dtype=np.float64)

# facem statisticile pe datele de antrenare
scaler = preprocessing.StandardScaler()
scaler.fit(x_train)  # calculeaza mean si standard deviation (Apelata DOAR PE DATELE DE ANTRENARE)

# afisam media
print(scaler.mean_)  # => [1.  0.  0.33333333]
# afisam deviatia standard
print(scaler.scale_)  # => [0.81649658 0.81649658 1.24721913]

# scalam datele de antrenare
scaled_x_train = scaler.transform(x_train)

print(scaled_x_train)  # => [[0.          -1.22474487  1.33630621]
#     [1.22474487   0.          -0.26726124]
#     [-1.22474487  1.22474487  -1.06904497]]

# scalam datele de test
scaled_x_test = scaler.transform(x_test)
print(scaled_x_test)  # => [[-2.44948974  1.22474487 -0.26726124]]

# In[13]:


# Scalarea intr-un anumit interval (de obicei vrem in intervalul [0,1])
x_train = np.array([[1, -1, 2], [2, 0, 0], [0, 1, -1]], dtype=np.float64)
x_test = np.array([[-1, 1, 0]], dtype=np.float64)

scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
scaler.fit(x_train)  # afla minimul si maximul

scaler.transform(x_train)


# In[14]:


# Normalizare L1, L2

# x_scaled = X/||X||1   L1
# x_scaled = X/||X||2   L2


# In[16]:


# SVM - Support Vector Machines

# 1. One vs All
# 2. One vs One
# Svm din sklearn foloseste one vs one


# In[2]:


def normalize_data(train_data, test_data, tip="l2"):
    if tip == "standard":
        scaler = preprocessing.StandardScaler()
        scaler.fit(train_data)

        scaled_x_train = scaler.transform(train_data)
        scaled_x_test = scaler.transform(test_data)
        return scaled_x_train, scaled_x_test

    if tip == "l1":
        scaler = preprocessing.Normalizer(norm='l1')
        scaler.fit(train_data)

        scaled_x_train = scaler.transform(train_data)
        scaled_x_test = scaler.transform(test_data)
        return scaled_x_train, scaled_x_test

    if tip == "l2":
        scaler = preprocessing.Normalizer(norm='l2')
        scaler.fit(train_data)

        scaled_x_train = scaler.transform(train_data)
        scaled_x_test = scaler.transform(test_data)
        return scaled_x_train, scaled_x_test


class BagOfWords:
    def __init__(self):
        self.voc = {}
        self.lst = []
        self.vocLen = 0

    def build_vocabulary(self, data):
        # data = [[st1],[st2],...[stn]]

        for line in data:
            for cuv in line:

                if cuv not in self.voc:
                    self.voc[cuv] = len(self.voc)
                    self.lst.append(cuv)

        self.vocLen = len(self.voc)

        print(self.vocLen)

    def get_features(self, data):
        # data = [[st1],[st2],...[stn]]

        features = np.zeros((len(data), self.vocLen))

        for doc_id, document in enumerate(data):
            for cuv in document:
                if cuv in self.voc:
                    features[doc_id, self.voc[cuv]] += 1

        return features


# In[4]:


bow = BagOfWords()

train_data = np.load("data1/training_sentences.npy", allow_pickle=True)
test_data = np.load("data1/test_sentences.npy", allow_pickle=True)
train_labels = np.load("data1/training_labels.npy", allow_pickle=True)
test_labels = np.load("data1/test_labels.npy", allow_pickle=True)

print(type(train_labels))
bow.build_vocabulary(train_data)

train_features = bow.get_features(train_data)
test_features = bow.get_features(test_data)

print(len(train_features[1]))

normalized_train, normalized_test = normalize_data(train_features, test_features, "l2")
print(len(normalized_train[1]))

svm_m = svm.SVC(C = 1,kernel = "linear")
fitted = svm_m.fit(normalized_train,train_labels)

predictions = fitted.predict(normalized_test)

print(f1_score(test_labels,predictions))


# In[1]:


cm = confusion_matrix(test_labels, predictions)

for i in cm:
    print(i)

coefs = np.array(svm_m.coef_)
idxs = np.argsort(coefs[0])

print(bow.lst[idxs])

# In[ ]:




