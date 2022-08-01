#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sklearn import preprocessing
from sklearn.metrics import f1_score
import numpy as np
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import ComplementNB
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import HalvingGridSearchCV
from sklearn.pipeline import Pipeline


# In[3]:


# Function for loading data from files
def load_data(fileName):
    path = "data/" + fileName
    data = []
    ids = []
    with open(path, encoding='utf-8') as f:
        line = f.readline()
        while line != '':
            line = line.replace('\n', '')
            x = line.split("	", 1)

            data.append(x[1])
            ids.append(x[0])
            line = f.readline()

    return data, ids


#function for loading the data labels
def load_labels(fileName):
    path = "data/" + fileName
    labels = []
    ids = []
    with open(path, encoding='utf-8') as f:
        line = f.readline()
        while line != '':
            x = [int(i) for i in line.split()]
            ids.append(x[0])
            labels.append(x[1])
            line = f.readline()

    return labels, ids


train_data, train_ids = load_data("train_samples.txt")
validation_data, validation_ids = load_data("validation_samples.txt")
test_data, test_ids = load_data("test_samples.txt")
train_labels, trids = load_labels("train_labels.txt")
validation_labels, veids = load_labels("validation_labels.txt")

#Combining train_data + validation data hopefully for a better score in competition
td = np.array(train_data + validation_data)
tl = np.array(train_labels + validation_labels)

#thought i will need the id-s for each test, but they were not really that necessary
train_ids = [int(i) for i in train_ids]
test_ids = [int(i) for i in test_ids]


train_data = np.array(train_data, dtype=object)
validation_data = np.array(validation_data,dtype=object)
test_data = np.array(test_data, dtype=object)
train_labels = np.array(train_labels)



# In[9]:


vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(2, 8),
    max_features=None,
    analyzer='char',
    binary=True,
    strip_accents='unicode',
)

# train_features = vectorizer.fit_transform(train_data)
# validation_features = vectorizer.transform(validation_data)
tf = vectorizer.fit_transform(td)
test_features = vectorizer.transform(test_data)

# In[12]:

nbm = LinearSVC()
nbm.fit(tf, tl)
predictions = nbm.predict(test_features)

# print(accuracy_score(predictions,validation_labels))

# In[13]:


with open("data/sample_submission.txt", 'w') as g:
    g.write("id,label\n")

    for i in range(len(predictions)):
        g.write(str(test_ids[i]) + "," + str(predictions[i]) + "\n")


# In[17]:


# Attempt of normalizing data before proceding to fit
def normalize_data(train_data, test_data, valid=None):
    scaler = preprocessing.Normalizer(norm="l2")
    scaler.fit(train_data)

    scaled_x_train = scaler.transform(train_data)
    scaled_x_test = scaler.transform(test_data)
    return scaled_x_train, scaled_x_test


norm_train, norm_test = normalize_data(train_features, validation_features)

# In[18]:
nbm = LinearSVC(random_state=0)
nbm.fit(norm_train, train_labels)
predictions = nbm.predict(norm_test)
print(accuracy_score(predictions, validation_labels))

# In[20]:

print(accuracy_score(predictions, validation_labels))

# In[ ]:
