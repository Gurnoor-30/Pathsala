# -*- coding: utf-8 -*-
"""maleria_detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/CaptaiN785/Maleria-detection/blob/main/maleria_detection.ipynb
"""

import zipfile
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import joblib
from glob import glob
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
from tensorflow.keras.applications import vgg19

file = zipfile.ZipFile("Dataset.zip")
file.extractall()
file.close()

train_dir = "/content/Dataset/Train"
test_dir = "/content/Dataset/Test"

par = 'Parasite'
non_par = "Uninfected"

category = par
cate_path = os.path.join(train_dir, category)
plt.figure(figsize=(12, 6))
for i, img_name in enumerate(os.listdir(cate_path)[:5]):
    plt.subplot(1, 5, i+1)
    img = plt.imread(os.path.join(cate_path, img_name)) 
    plt.imshow(img)
    plt.axis("off")
    plt.title(category)
plt.show()

category = non_par
cate_path = os.path.join(train_dir, category)
plt.figure(figsize=(12, 6))
for i, img_name in enumerate(os.listdir(cate_path)[:5]):
    plt.subplot(1, 5, i+1)
    img = plt.imread(os.path.join(cate_path, img_name)) 
    plt.imshow(img)
    plt.axis("off")
    plt.title(category)
plt.show()

images = glob(train_dir+"/*/*", recursive=True)
len(images)

test_image = glob(test_dir + "/*/*")
len(test_image)

train_gen = ImageDataGenerator(
    rescale = 1.0/255.0,
    horizontal_flip=True,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2
)

test_gen = ImageDataGenerator(
    rescale=1.0/255.0
)

batch_size = 16
st_per_ep = len(images)/batch_size
val_step = len(test_image)/batch_size

train_set = train_gen.flow_from_directory(
    train_dir,
    target_size=(96, 96),
    class_mode = 'binary',
    batch_size = batch_size
)
test_set = test_gen.flow_from_directory(
    test_dir,
    target_size=(96, 96),
    class_mode = 'binary',
    batch_size=batch_size
)

model = models.Sequential([
    layers.Input(shape=(96, 96, 3)),
    layers.Conv2D(64, (5, 5), strides=(2, 2), padding='same', activation='relu'),
    layers.Conv2D(64, (5, 5), padding='same', activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.2),

    layers.Conv2D(128, (3, 3), padding = "same", activation = 'relu'),
    layers.Conv2D(128, (3, 3), padding = "same", activation = 'relu'),
    layers.Conv2D(128, (3, 3), padding = "same", activation = 'relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.2),

    layers.Conv2D(256, (3, 3), activation = 'relu', padding = "same"),
    layers.Conv2D(256, (3, 3), activation = 'relu', padding = "same"),
    layers.Conv2D(256, (3, 3), activation = 'relu', padding = "same"),
    layers.Conv2D(256, (3, 3), activation = 'relu', padding = "same"),
    layers.Conv2D(256, (3, 3), activation = 'relu', padding = "same"),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    
    layers.Flatten(),
    layers.Dropout(0.2),
    layers.Dense(512, activation = 'relu'),
    layers.Dense(1, activation = 'sigmoid')
])
model.summary()

from tensorflow.keras.optimizers import Adam
adam = Adam(learning_rate = 0.0001)
model.compile(optimizer = adam, loss = 'binary_crossentropy', metrics = ['accuracy'])

history = model.fit(
    train_set, 
    steps_per_epoch=st_per_ep,
    validation_data = test_set,
    validation_steps=val_step,
    epochs = 100,
)

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title("Loss graph")
plt.legend(['loss', 'val_loss'])
plt.show()

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title("Accurac graph")
plt.legend(['accuracy', 'val_accuracy'])
plt.show()

import cv2 as cv

type(accuracy)
x = history.history["accuracy"]
actual_accuracy = sum(x)/len(x)
print(actual_accuracy)

img_path = "/content/Dataset/Test/Parasite/C39P4thinF_original_IMG_20150622_105554_cell_10.png"
par_img = cv.imread(img_path)
par_img.shape

img_rgb = cv.cvtColor(par_img,cv.COLOR_BGR2RGB)
plt.imshow(img_rgb)
plt.show()
img_rgb = cv.resize(par_img, (96, 96))
plt.imshow(img_rgb)
plt.show()

img = np.expand_dims(img_rgb, 0)

model.predict(img)

train_set.class_indices

def Predict(image_path):
    images = []
    corrupted_index = []
    for i, img_path in enumerate(image_path):
        try:
            img = cv.imread(img_path)
            img = cv.resize(img, (96, 96), interpolation=cv.INTER_AREA)/255.0
            images.append(img)
        except:
            corrupted_index.append(i)
    images = np.array(images)
    print("Shape of array is : ", images.shape)
    result = model.predict(images)
    return {"result":np.round(result[:, 0]), "error_index":corrupted_index}

par_dir = os.path.join(test_dir, par)
par_images = os.listdir(par_dir)

par_dirs = []
for img_name in par_images:
    par_dirs.append(os.path.join(par_dir, img_name))

non_par_dir = os.path.join(test_dir, non_par)
non_par_images = os.listdir(non_par_dir)

non_par_dirs = []
for img_name in non_par_images:
    non_par_dirs.append(os.path.join(non_par_dir, img_name))

result = Predict(par_dirs)

result['result'], result['error_index']

1 - (result['result'].sum()/len(par_dirs))

result = Predict(non_par_dirs)

result['result'].sum()/len(non_par_dirs)



def Predict_One(image_path):

    label = {0:"Parasite", 1:"Uninfected"}

    img = cv.imread(image_path)
    img = cv.resize(img, (96, 96), interpolation=cv.INTER_AREA)/255.0
    img = np.expand_dims(img, 0)

    print("Shape of array is : ", img.shape)
    result = model.predict(img)
    return label[np.round(result[0][0])]

Predict_One("/content/Dataset/Test/Parasite/C39P4thinF_original_IMG_20150622_105554_cell_13.png")

Predict_One("/content/Dataset/Test/Uninfected/C3thin_original_IMG_20150608_163002_cell_159.png")

model.save("model.hd5")

md = models.load_model("model.hd5")

def Predict_One_saved(image_path):

    label = {0:"Parasite", 1:"Uninfected"}

    img = cv.imread(image_path)
    img = cv.resize(img, (96, 96), interpolation=cv.INTER_AREA)/255.0
    img = np.expand_dims(img, 0)

    print("Shape of array is : ", img.shape)
    result = md.predict(img)
    return label[np.round(result[0][0])]

Predict_One_saved("/content/Dataset/Test/Parasite/C39P4thinF_original_IMG_20150622_105554_cell_13.png")

Predict_One_saved("/content/Dataset/Test/Uninfected/C3thin_original_IMG_20150608_163002_cell_159.png")

