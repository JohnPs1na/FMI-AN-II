#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn import preprocessing
from sklearn.metrics import f1_score

# definirea modelelor
linear_regression_model = LinearRegression()
# calcularea valorii MSE și MAE
from sklearn.metrics import mean_squared_error, mean_absolute_error

# In[2]:


import numpy as np
from sklearn.utils import shuffle

# load training data
training_data = np.load('data/training_data.npy')
prices = np.load('data/prices.npy')
print('The first 4 samples are:\n ', training_data[:4])
print('The first 4 prices are:\n ', prices[:4])
# shuffle
training_data, prices = shuffle(training_data, prices, random_state=0)


# In[17]:


def normalizeData(train_data, test_data=None):
    scaler = preprocessing.StandardScaler()
    scaler.fit(train_data)

    scaled_x_train = scaler.transform(train_data)

    if test_data == None:
        return scaled_x_train

    scaled_x_test = scaler.transform(test_data)
    return scaled_x_train, scaled_x_test


# n = len(training_data)

# train_data = training_data[:n//2]
# test_data = train_data[n//2:]
# prices_train = prices[:n//2]
# prices_test = prices[n//2:]

# sc_train,sc_test = normalizeData(train_data,test_data)

# linear_regression_model.fit(train_data,prices_train)

# predictions = linear_regression_model.predict(test_data)

# print(f1_score(prices_test,predictions))


# In[20]:


# impart datele
nspf = len(training_data) // 3

train_data1, prices1 = training_data[:nspf], prices[:nspf]
train_data2, prices2 = training_data[nspf:2 * nspf], prices[nspf:2 * nspf]
train_data3, prices3 = training_data[2 * nspf:], prices[2 * nspf:]


# In[5]:


def train_model(model, train_data, train_labels, test_data, test_labels):
    model.fit(train_data, train_labels)
    predictions = model.predict(test_data)

    mse = mean_squared_error(predictions, test_labels)
    mae = mean_absolute_error(predictions, test_labels)

    return mae, mse


# In[6]:


mae1, mse1 = train_model(linear_regression_model, np.concatenate((train_data1, train_data2)),
                         np.concatenate((prices1, prices2)), train_data3, prices3)
mae2, mse2 = train_model(linear_regression_model, np.concatenate((train_data1, train_data3)),
                         np.concatenate((prices1, prices3)), train_data2, prices2)
mae3, mse3 = train_model(linear_regression_model, np.concatenate((train_data2, train_data3)),
                         np.concatenate((prices2, prices3)), train_data1, prices1)

print("Mean Mae = ", (mae1 + mae2 + mae3) / 3)
print("Mean Mse = ", (mse1 + mse2 + mse3) / 3)

# In[10]:


alphas = [1, 10, 100, 1000]
ridge_regression_model = Ridge(alpha=1)

for a in alphas:
    ridge_regression_model.alpha = a
    mae1, mse1 = train_model(ridge_regression_model, np.concatenate((train_data1, train_data2)),
                             np.concatenate((prices1, prices2)), train_data3, prices3)
    mae2, mse2 = train_model(ridge_regression_model, np.concatenate((train_data1, train_data3)),
                             np.concatenate((prices1, prices3)), train_data2, prices2)
    mae3, mse3 = train_model(ridge_regression_model, np.concatenate((train_data2, train_data3)),
                             np.concatenate((prices2, prices3)), train_data1, prices1)

    print("Mean Mae=", (mae1 + mae2 + mae3) / 3)
    print("Mean Mse=", (mse1 + mse2 + mse3) / 3)

# In[21]:


train_data = normalizeData(training_data)
model = Ridge(alpha=10)

model.fit(train_data, prices)

coef = model.coef_

cel_mai_smecher = np.argmax(np.abs(coef))

lista_de_indici_sortate = np.argsort(np.abs(coef))

print(coef[cel_mai_smecher])
print(coef[lista_de_indici_sortate[-2]])
print(coef[lista_de_indici_sortate[0]])

# In[ ]:




