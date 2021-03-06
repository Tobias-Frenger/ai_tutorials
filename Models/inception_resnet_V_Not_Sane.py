# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 17:25:33 2020

@author: Tobias
"""

from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D, BatchNormalization, AveragePooling2D, Add
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.models import Sequential, Model
from glob import glob

import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import pickle
import cv2

import pydot
import os

from tensorflow.keras.backend import sigmoid

def swish(x, beta = 1):
    return (x * sigmoid(beta*x))

from tensorflow.keras.utils.generic_utils import get_custom_objects
from tensorflow.keras.layers import Activation
get_custom_objects().update({'swish': Activation(swish)})

#TRAINING DATA
pickle_in = open("C:/Users/Tobias/CNN/Thesis_Models/Saved_Datasets/Boats/training_set_X.pickle", "rb")
train_x = pickle.load(pickle_in)
#Answers to training data
pickle_in = open("C:/Users/Tobias/CNN/Thesis_Models/Saved_Datasets/Boats/training_set_y.pickle", "rb")
train_y = pickle.load(pickle_in)

#TEST DATA
pickle_in = open("C:/Users/Tobias/CNN/Thesis_Models/Saved_Datasets/Boats/test_set_X.pickle", "rb")
test_x = pickle.load(pickle_in)
#Answers to training data
pickle_in = open("C:/Users/Tobias/CNN/Thesis_Models/Saved_Datasets/Boats/test_set_y.pickle", "rb")
test_y = pickle.load(pickle_in)

#Normalize data -- scale the data
train_x = train_x/255.0
test_x = test_x/255.0
train_y = np.array(train_y)
test_y = np.array(test_y)

def conv_block(X, filters, kernel_size, strides):
    shortcut = X
    if strides == 1:
        while (kernel_size > 1): # replacing the kernel_size with 3x3 kernels to cover the same area while saving in computational cost
            X = Conv2D(filters, kernel_size=3, strides=1, padding = 'same')(X)
            kernel_size = ((kernel_size - 3)/1) + 1
    else:
        X = Conv2D(filters, kernel_size=kernel_size, strides=strides, padding = 'same')(X)
    #shortcut = AveragePooling2D(pool_size=kernel_size, strides = 1)
    X = Add()([shortcut, X])
    X = common_layers(X)
    return X
    
def common_layers(X):
    X = BatchNormalization()(X)
    X = tf.keras.layers.LeakyReLU()(X)
    return X
    
def conv_layer(X, filters, kernel_size, strides):
    shortcut = X
    if strides == 1:
        while (kernel_size > 1): # replacing the kernel_size with 3x3 kernels to cover the same area while saving in computational cost
            X = Conv2D(filters, kernel_size=3, strides=1, padding = 'same')(X)
            kernel_size = ((kernel_size - 3)/1) + 1
    else:
        X = Conv2D(filters, kernel_size=kernel_size, strides=strides, padding = 'same')(X)
    #shortcut = AveragePooling2D(pool_size=kernel_size, strides = 1)
    X = Add()([shortcut, X])
    return X

def maxPool_layer(X, pool_size, strides):
    X = MaxPooling2D(pool_size = pool_size, strides = strides, padding = "valid")(X)
    return X

def inception_block(X, filters):
    split_1 = int(filters/4)
    split_2 = int(filters/2)
    l1 = Conv2D(split_1, 1, 1, padding='same')(X)
    l1 = conv_layer(l1, split_1, 11, 1)
    l2 = Conv2D(split_1, 1, 1, padding='same')(X)
    l2 = conv_layer(l2, split_1, 7, 1)
    l3 = Conv2D(split_2, 1, 1, padding='same')(X)
    l3 = conv_layer(l3, split_2, 7, 1)
    X = tf.keras.layers.concatenate([l1,l2,l3])
    X = tf.keras.layers.LeakyReLU()(X)
    return X

def residual_block(X, filters):
    shortcut = X
    X = conv_layer(X, filters, 11, 1)
    X = conv_block(X, filters, 7, 1)
    X = Add()([shortcut, X])
    X = tf.keras.layers.LeakyReLU()(X)
    X = conv_layer(X, filters, 5, 1)
    X = BatchNormalization()(X)
    X = conv_layer(X, filters, 3, 1)
    X = Add()([shortcut, X])
    X = common_layers(X)
    return X

def res_model():
    inputs = tf.keras.Input(shape=(128,128,3))
    X = Conv2D(24, 1, 1, padding='same')(inputs)
    X = maxPool_layer(X, 3, 3)
    X = residual_block(X, 24)
    X = Conv2D(16, 3, 3, padding='same')(X)
    X = inception_block(X, 16)
    
    X = maxPool_layer(X, 3, 3)
    X = Flatten()(X)
    X = Dense(5)(X)
    outputs = Activation("softmax")(X)
    model = tf.keras.Model(inputs = inputs, outputs = outputs, name ="res_model")
    model.compile(loss="sparse_categorical_crossentropy", optimizaer="adam", metrics=['accuracy'])
    return model

res_model = res_model()
res_model.summary()
res_model.save("C:/Users/Tobias/CNN/Thesis_Models/res_model/" + res_model.name + ".hdf5")
#DISPLAY MODEL STRUCTURE
tf.keras.utils.plot_model(res_model, 'my_first_model_with_shape_info.png', show_shapes=True)
#res_model.metrics_names
#PREPARE TRAINING
checkpoint_loss = ModelCheckpoint('C:/Users/Tobias/CNN/Thesis_Models/' + str(res_model.name) + '/saved_models/' + res_model.name + '_{epoch:02d}-{loss:.2f}_best_model.hdf5', monitor='loss', verbose=1, save_best_only=True, mode='auto', period=1)
checkpoint_val_loss = ModelCheckpoint('C:/Users/Tobias/CNN/Thesis_Models/' + str(res_model.name) + '/saved_models/' + res_model.name + '_{epoch:02d}-{loss:.2f}_best_val_model.hdf5', monitor='val_loss', verbose=1, save_best_only=True, mode='auto', period=1)
reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.1, patience=10, verbose=0, mode='auto', min_delta=0.0001, cooldown=0, min_lr=0.001)
#TRAIN THE MODEL AND STORE THE RESULTS
history = res_model.fit(train_x, train_y, batch_size=16, validation_split=0.10, epochs = 10, callbacks=[checkpoint_loss, checkpoint_val_loss, reduce_lr])

#USE FOR LATER
#from model_training_script import train_model
#history = train_model('C:/Users/Tobias/CNN/Thesis_Models/res_model/' + res_model.name + '.hdf5', train_x, train_y)

#SHOW TRAINING RESULTS
def show(history):
    val_acc = history['val_accuracy']
    val_loss = history['val_loss']
    acc = history['accuracy']
    loss = history['loss']
    epochs = range(len(acc))
    plt.plot(epochs, acc, 'b', label='Training acc')
    plt.plot(epochs, loss, 'c', label='Training loss')
    plt.plot(epochs, val_acc, 'r', label='Validation acc')
    plt.plot(epochs, val_loss, 'g', label='Validation loss')
    plt.legend()
    plt.ylim(top=1.5, bottom=0.0)
    plt.figure()
    plt.show()

show(history.history)

#MODEL EVALUATION
res_model.load_weights('C:/Users/Tobias/CNN/Thesis_Models/res_model/saved_models/s1/res_model_09-0.38_best_val_model.hdf5')
res_model.evaluate(test_x, test_y, batch_size=32, verbose=2)

#VALIDATION OF RESULTS
#Heatmap
res_model.summary()
from grad_cam import grad_cam
#IMAGE = 'C:/Users/Tobias/CNN/Labbdata_spectrogram_2500ms/Sub/Red_Hat1-3145.jpg'
IMAGE = 'C:/Users/Tobias/CNN/Labbdata_spectrogram_2500ms/Tugboat/Tugboat1-340112.jpg'
#IMAGE = 'C:/Users/Tobias/CNN/Images/Trafik/trafik_tva_43.jpg'
layer_name = "conv2d_20"
alpha=0.9
grad_cam(res_model, layer_name, IMAGE, alpha)
#Print with alpha 0.5 and alpha 1.0
def printHMvariations(layer, img):
    IMG = cv2.imread(img, cv2.IMREAD_UNCHANGED)
    IMG = cv2.cvtColor(IMG, cv2.COLOR_BGR2RGB)
    alpha=1.0
    for i in range(2):
        grad_cam(res_model, layer, img, alpha)
        alpha -= 0.5
    IMG = cv2.imread(IMAGE, cv2.IMREAD_UNCHANGED)
    IMG = cv2.cvtColor(IMG, cv2.COLOR_BGR2RGB)
    plt.imshow(IMG)
    plt.show()

printHMvariations(layer_name, IMAGE)

def displayImage(img):
    IMG = cv2.imread(img, cv2.IMREAD_UNCHANGED)
    IMG = cv2.cvtColor(IMG, cv2.COLOR_BGR2RGB)
    plt.imshow(IMG)
    plt.show()
    
displayImage(IMAGE)
