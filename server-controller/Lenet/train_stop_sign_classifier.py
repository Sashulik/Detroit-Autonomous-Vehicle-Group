import csv
import numpy as np
from random import shuffle
import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras import applications
from keras.backend import clear_session
import h5py as h5py
import pickle
from keras.layers.convolutional import Conv2D, Cropping2D
from keras.layers import Input
from keras.layers.pooling import MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
import keras.backend
from keras.layers import Lambda
from keras.regularizers import l2
import scipy

training_file = 'dataset/train.p'
testing_file = 'dataset/test.p'
validation_file = 'dataset/valid.p'

with open(training_file, mode='rb') as f:
	train = pickle.load(f)
with open(validation_file, mode='rb') as f:
	valid = pickle.load(f)
with open(testing_file, mode='rb') as f:
	test = pickle.load(f)
	
X_train, y_train = train['features'], train['labels']
X_valid, y_valid = valid['features'], valid['labels']
X_test, y_test = test['features'], test['labels']

# change the labels to be stop: 1 non-stop: 0
for labels in [y_train, y_valid, y_test]:
	for i in range(len(labels)):
		if labels[i] != 14:
			labels[i] = 0
		else:
			labels[i] = 1


def normalize(image):
	return image/255.0 - 0.5
	
def train_model():
	
	print("starting trainning model")
	model = Sequential()
	model.add(Lambda(normalize, input_shape=(32, 32, 3)))
	print("input layer:", model.layers[-1].output_shape)
	
	model.add(Conv2D(6, (6, 6), strides=(2,2), kernel_regularizer=l2(0.0005), activation='relu'))
	print("conv 1 layer:", model.layers[-1].output_shape)
	
	model.add(Conv2D(16, (5, 5), strides=(2,2), kernel_regularizer=l2(0.0005), activation='relu'))
	print("conv 2 layer:", model.layers[-1].output_shape)
	
	model.add(Flatten())
	model.add(Dense(120, kernel_regularizer=None))
	model.add(Dense(84, kernel_regularizer=None))
	model.add(Dense(1, kernel_regularizer=None))
	model.compile(optimizer='adam', loss='mse')
	
	batch_size = 128
	
	model.fit(X_test, y_test, batch_size=batch_size, epochs=10, verbose=1, callbacks=None, validation_data=(X_valid, y_valid), shuffle=True, class_weight=None, sample_weight=None, initial_epoch=0)
	model.save("model.h5")
	print("saving trainning model")

train_model()
