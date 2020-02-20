# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 00:16:11 2020

@author: Tobias
"""

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from matplotlib.pyplot import imread, imshow, subplots, show
import os
from glob import glob

def plot(data_generator):
    """
    Plots 4 images generated by an object of the ImageDataGenerator class.
    """
    data_generator.fit(images)
    image_iterator = data_generator.flow(images)
    
    # Plot the images given by the iterator
    fig, rows = subplots(nrows=1, ncols=2, figsize=(128,128))
    for row in rows:
        row.imshow(image_iterator.next()[0].astype('int'))
        row.axis('off')
    #show()
    
image = imread('C:/dir/to/images/image.jpg')

# Creating a dataset which contains just one image.
images = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))

imshow(images[0])
show()

data_generator = ImageDataGenerator(rotation_range=90)
plot(data_generator)

data_generator = ImageDataGenerator(width_shift_range=0.3)
plot(data_generator)

data_generator = ImageDataGenerator(height_shift_range=0.2)
plot(data_generator)

data_generator = ImageDataGenerator(brightness_range=(0.1, 0.9))
plot(data_generator)

data_generator = ImageDataGenerator(shear_range=45.0)
plot(data_generator)

data_generator = ImageDataGenerator(zoom_range=[0.5, 1.25])
plot(data_generator)

data_generator = ImageDataGenerator(channel_shift_range=150.0)
plot(data_generator)

data_generator = ImageDataGenerator(horizontal_flip=True)
plot(data_generator)

data_generator = ImageDataGenerator(vertical_flip=True)
plot(data_generator)

data_generator = ImageDataGenerator(width_shift_range=0.3, fill_mode='nearest')
plot(data_generator)

data_generator = ImageDataGenerator(width_shift_range=0.3, fill_mode='reflect')
plot(data_generator)

data_generator = ImageDataGenerator(width_shift_range=0.3, fill_mode='wrap')
plot(data_generator)

data_generator = ImageDataGenerator(width_shift_range=0.3, 
                                    fill_mode='constant', 
                                    cval=190)
plot(data_generator)
os.mkdir('C:/your/new/directory')
def augmented_images(data_generator):
        data_generator.fit(images)
    image_iterator = data_generator.flow(images)
    
    # Plot the images given by the iterator
    fig, rows = subplots(nrows=1, ncols=3, figsize=(128,128))
    for row in rows:
        row.imshow(image_iterator.next()[0].astype('int'))
        row.axis('off')
    show()
    Data_dir=np.array(glob('C:/dir/to/images/*'))
    CATEGORIES = ["knight", "orc", "sorceress"]

    
    for image in Data_dir:
        print (image)
        image = imread('C:/dir/to/images/*')
    
    # Creating a dataset which contains just one image.
    images = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    i = 0
    range = 4
    for index in range(range):
        if (i <= 4):
            #request with 2 sec timeout
            with open("C:/folder/filename_"+str(index+1)+'.jpg', 'wb+') as f:
                f.write(img_data)
            i += 1
        else:
            f.close()
            break