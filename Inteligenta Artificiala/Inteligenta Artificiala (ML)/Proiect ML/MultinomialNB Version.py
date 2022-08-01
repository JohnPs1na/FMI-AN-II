#!/usr/bin/env python
# coding: utf-8

# In[126]:


from sklearn import preprocessing
from sklearn.metrics import f1_score
import numpy as np
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


# from tensorflow.python.keras.preprocessing import text


# In[2]:


def normalize_data(train_data, test_data, valid=None):
    scaler = preprocessing.Normalizer(norm="l2")
    scaler.fit(train_data)

    scaled_x_train = scaler.transform(train_data)
    scaled_x_test = scaler.transform(test_data)
    return scaled_x_train, scaled_x_test


# In[311]:


# input
def load_data(fileName):
    path = "data/" + fileName
    data = []
    ids = []
    with open(path, encoding='utf-8') as f:
        line = f.readline()
        while line != '':
            x = line.split("	", 1)

            data.append(x[1])
            ids.append(x[0])
            line = f.readline()

    return data, ids


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

td = np.array(train_data + validation_data)
tl = np.array(train_labels + validation_labels)

train_ids = [int(i) for i in train_ids]
test_ids = [int(i) for i in test_ids]

train_data = np.array(train_data, dtype=object)
validation_data = np.array(validation_data,dtype=object)
test_data = np.array(test_data, dtype=object)
train_labels = np.array(train_labels)


# In[4]:

# In[358]:

#Attempt of Using Halving Grid Search on a CountVectorizer() MultinomialNB pipeline
pipeline = Pipeline([("vect", CountVectorizer()), ("clf", MultinomialNB())])

#sparse as much parameters as i can so it will find the most optimal version of predicting data
parameters = {
    "vect__decode_error": ('strict', 'ignore', 'replace'),
    "vect__lowercase": (True, False),
    "vect__binary": (True, False),
    "vect__ngram_range": ((1, 3), (2, 5), (1, 7), (1, 6)),
    "vect__analyzer": ('char','word'),
    "vect__strip_accents": ('unicode', None,'ascii'),
    'clf__alpha': (0.1, 0.5, 1),
}
grid_search = HalvingGridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1)

# In[9]:
resultSearch = grid_search.fit(train_data, train_labels)

# In[10]:

params = grid_search.best_estimator_.get_params()
for i in params:
    print(i, params[i])


# In[326]:

vectorizer = CountVectorizer(
    lowercase=False,
    ngram_range=(1, 7),
    max_features=None,
    analyzer='char',
    binary=True,
    decode_error='strict'
)

# vectorizer = TfidfVectorizer(decode_error='strict',
#                              strip_accents=None,
#                              lowercase=True,
#                              max_df=0.75,
#                              min_df=0.001,
#                              ngram_range=(1,1),
#                              max_features=None,
#                              )

train_features = vectorizer.fit_transform(train_data)
validation_features = vectorizer.transform(validation_data)
# tf = vectorizer.fit_transform(td)
test_features = vectorizer.transform(test_data)

# In[ ]:


# In[355]:

nbm = MultinomialNB(alpha=0.1)
nbm.fit(tf, tl)
predictions = nbm.predict(test_features)
# print(accuracy_score(predictions, validation_labels))

# In[315]:

with open("data/sample_submission.txt", 'w') as g:
    g.write("id,label\n")

    for i in range(len(predictions)):
        g.write(str(test_ids[i]) + "," + str(predictions[i]) + "\n")

# In[300]:

print(grid_search.best_score_)






