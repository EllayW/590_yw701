#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from keras.datasets import boston_housing
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras import models
from keras import layers
import numpy as np
import matplotlib.pyplot as plt
from keras.optimizers import SGD
from keras.regularizers import l1, l2
from keras.datasets import mnist
from keras.datasets import fashion_mnist
from keras.models import load_model


# In[2]:


################################################################
####################### Training ###############################
################################################################


# In[43]:


### define hyperparameters:
#f1=lambda NKEEP: int(0.01*NKEEP)
epochs=20
optimizer = 'rmsprop'
learning_rate = .01
LASSO = l1(learning_rate)
RIDGE = l2(learning_rate)
loss = 'mean_squared_error'
regulation = LASSO
batch_size=1000
n_bottleneck = 100


# In[44]:


### read the input:
(X, Y), (test_images, test_labels) = mnist.load_data()


# In[45]:


### normalization:
X = X.astype('float32') / 255.
test_images = test_images.astype('float32') / 255.


### flattening:
X = X.reshape((len(X), np.prod(X.shape[1:])))
test_images = test_images.reshape((len(test_images), np.prod(test_images.shape[1:])))


# In[6]:


### build the base model:
def DAE():
    model = models.Sequential()
    model.add(layers.Dense(n_bottleneck, activation='relu', input_shape=(28 * 28,)))
    model.add(layers.Dense(28*28,  activation='relu'))
    return(model)

### compile the model:
def final_model(mod):
    mod.compile(optimizer=optimizer,
                      loss=loss)
    return(mod)

### evaluate the model:
def evaluation(mod,X,vis=True):
    global train_mse_histories
    global val_mse_histories
    
    train_mse_histories = []
    val_mse_histories = []
    
    history = mod.fit(X, X,validation_split=0.2,
        epochs=epochs, batch_size=batch_size)

    val_mse_history = history.history['val_loss']
    train_mse_history = history.history['loss']
    train_mse_histories.append(train_mse_history)
    val_mse_histories.append(val_mse_history)
        
    average_val_mse_history = [np.mean([x[i] for x in val_mse_histories])             for i in range(epochs)]
    average_train_mse_history = [np.mean([x[i] for x in train_mse_histories])             for i in range(epochs)]
    
    save_name = 'HW6.1-ae.h5'
    mod.save(save_name)
    ## visualizations:
    if vis:
        plt.plot(range(1, len(average_val_mse_history) + 1), average_val_mse_history)
        plt.plot(range(1, len(average_train_mse_history) + 1),average_train_mse_history)
    return([average_val_mse_history,average_train_mse_history])


# In[9]:


### Build the model:
model = DAE()
model = final_model(model)
avg_val,avg_train = evaluation(model,X)
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title("Validation/Train MSE")
plt.legend(['validation', 'train'], loc='upper left')
plt.show()


# In[10]:


### print out the model summary:
plt.savefig('HW6.1-train-val-loss.png')
model.summary()
model = load_model('HW6.1-ae.h5')
model.evaluate(X,X,batch_size = batch_size)


# In[11]:


model.evaluate(test_images,test_images,batch_size = batch_size)


# In[56]:


################################################################
####################### Fashion Data ###########################
################################################################


# In[36]:


(X_fas, Y_fas), (test_images_fas, test_labels_fas) = fashion_mnist.load_data()


# In[37]:


### normalization:
X_fas = X_fas.astype('float32') / 255.
#test_images_fas = test_images_fas.astype('float32') / 255.

### flattening:
X_fas = X_fas.reshape((len(X_fas), np.prod(X_fas.shape[1:])))
#test_images_fas= test_images_fas.reshape((len(test_images_fas), np.prod(test_images_fas.shape[1:])))


# In[46]:


### visualize the input/output:
X1=model.predict(test_images)
X2 = model.predict(X_fas)
test_images=test_images.reshape(10000,28,28)
X1=X1.reshape(10000,28,28)
X2=X2.reshape(60000,28,28)

f, ax = plt.subplots(6,1)
I1=1
I2=2
ax[0].imshow(test_images[I1])
ax[1].imshow(X1[I1])
ax[2].imshow(test_images[I2])
ax[3].imshow(X1[I2])
ax[4].imshow(X2[I1])
ax[5].imshow(X2[I2])
plt.show()


# In[47]:


f.savefig('HW6.1-history.png')


# In[48]:


### define threshold:
thres = 4*model.evaluate(X,X,batch_size = batch_size)


# In[49]:


def count_anomaly(dataset):
    ## dataset = X_fas or X
    count = 0
    for i in range(dataset.shape[0]):
        dat = dataset[i].reshape(1,784)
        err = model.evaluate(dat,dat)
        if err > thres:
            count +=1
    return(count)


# In[50]:


### count anomalies in the train dataset
count_anomaly(X)


# In[51]:


### count anomalies in the anomaly dataset
count_anomaly(X_fas)


# In[ ]:




