#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import matplotlib.pyplot as plt


# In[3]:


l = np.array([1,2,3])
print(type(l))
print(l.shape)

matrix = np.array([[1,2],[3,4]])

print(matrix.shape[0])


# In[10]:


zero = np.zeros((2,2))
print(zero)


# In[12]:


id = np.eye(3)
print(id)


# In[14]:


first_5 = np.arange(1,6)
print(first_5)


# In[15]:


new_m = np.full((2,2),8)
print(new_m)


# In[17]:


randoms = np.random.random((2,3))
print(randoms)


# In[18]:


gauss = np.random.normal(0,0.1,(2,3))
print(gauss)


# In[22]:


m = np.eye(3)
new_m = np.copy(m[0:2,0:2])
new_m[0,0] = 100

nlist_m = np.ravel(m)
print(nlist_m)

m1 = np.reshape(nlist_m,(3,3))
print(m1)


# In[25]:


l = np.array([1,2,3,4])
print(l>2)
print(l[l>2])


# In[49]:


a = np.array([[1,2],[3,4]])
b = np.array([[5,6],[7,8]])

c = np.dot(a,b)
x = np.matmul(a,b)
print(c)
print(x)
print(a.T)  #transpusa
# print(np.linalg.inv(a))

d = np.array([[1,2,3],[4,5,6]])

np.mean(d,axis = (0,1))


# In[44]:


l = np.array([3,5,9,0,1])
np.argmax(l)
np.argmin(l)


# In[12]:


x = np.arange(0,3*np.pi,0.1)
y = np.sin(x)
y1 = np.cos(x)
plt.plot(x,y1)
plt.plot(x,y)
plt.show()


# In[18]:


images = np.zeros((9,400,600))
number = 9
for i in range(number):
    image = np.load(f'images/car_{i}.npy')
    images[i] = image

print(np.argmax(np.sum(images,axis = (1,2))))

mean_image = np.mean(images,axis = 0)
plt.plot(mean_image)
plt.show()

from skimage import io
io.imshow(mean_image.astype(np.uint8))
io.show()

# f
devstd = np.std(images)
print('deviatia standard ',devstd)

# g
for idx, image in enumerate(images):
    normalized_image = (image - mean_image) / devstd
    io.imshow(normalized_image.astype(np.uint8))
    io.show()

# h
for idx, image in enumerate(images):
    new_img = image[200:300, 280:400]
    io.imshow(new_img.astype(np.uint8))
    io.show()


# In[ ]:




