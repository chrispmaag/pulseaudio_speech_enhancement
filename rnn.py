#!/usr/bin/env python
# coding: utf-8

# In[1]:

import sys
import glob
import numpy as np
import tensorflow as tf
from datetime import datetime
from scipy.io import wavfile
from random import sample


# In[2]:


TRAINING_SET_SIZE = 11572
TEST_SET_SIZE = 824
FRAME_RATE = 48000

WINDOW_LENGTH_MILISECONDS = 40
WINDOW_SHIFTS_MILISECONDS = 16

TRAIN_SET_NOISY = './data/noisy_trainset_28spk_wav/*.wav'
TRAIN_SET_CLEAN = './data/clean_trainset_28spk_wav/*.wav'

TEST_SET_NOISY  = './data/noisy_testset_wav/*.wav'
TEST_SET_CLEAN  = './data/clean_testset_wav/*.wav'

EPOCHS = 2

# In[3]:


sequence_length = int(FRAME_RATE*WINDOW_LENGTH_MILISECONDS/1000)
sequence_shift  = int(FRAME_RATE*WINDOW_SHIFTS_MILISECONDS/1000)

print(sequence_length, sequence_shift)


# In[4]:


def min_max_scaling(Z):
    """[summary]

    Args:
        Z ([type]): [description]

    Returns:
        [type]: [description]
    """
    return (Z - np.min(Z))/np.ptp(Z)


def window_generator(path_to_noisy_files: np.array, path_to_clean_files: np.array, shift, length, limit=sys.maxsize):
    """[summary]

    Args:
        path_to_noisy_files (np.array): [description]
        path_to_clean_files (np.array): [description]
        shift ([type]): [description]
        length ([type]): [description]

    Yields:
        [type]: [description]
    """
    noisy_filenames = glob.glob(path_to_noisy_files)[:limit]
    clean_filenames = glob.glob(path_to_clean_files)[:limit]

    noisy_data = [wavfile.read(file)[1] for file in noisy_filenames]
    clean_data = [wavfile.read(file)[1] for file in clean_filenames]

    while True:
        for i in sample(list(range(len(noisy_data))), len(noisy_data)):
            X_i = []
            Y_i = []
            for j in range((len(noisy_data[i]) - length)//shift + 1):
                X_i.append(min_max_scaling(noisy_data[i][j*shift: j*shift + length]))
                Y_i.append(min_max_scaling(clean_data[i][j*shift: j*shift + length]))
            yield np.array(X_i), np.array(Y_i)


def window_dataset(path_to_noisy_files: np.array, path_to_clean_files: np.array, shift, length, batch_size=128, buffer_size=100, limit=sys.maxsize):
    """[summary]

    Args:
        path_to_noisy_files (np.array): [description]
        path_to_clean_files (np.array): [description]
        shift ([type]): [description]
        length ([type]): [description]

    Yields:
        [type]: [description]
    """
    noisy_filenames = glob.glob(path_to_noisy_files)[:limit]
    clean_filenames = glob.glob(path_to_clean_files)[:limit]

    noisy_data = [wavfile.read(file)[1] for file in noisy_filenames]
    clean_data = [wavfile.read(file)[1] for file in clean_filenames]

    X = []
    Y = []

    for i in range(len(noisy_data)):
        for j in range((len(noisy_data[i]) - length)//shift + 1):
            X.append(min_max_scaling(noisy_data[i][j*shift: j*shift + length]))
            Y.append(min_max_scaling(clean_data[i][j*shift: j*shift + length]))

    dataset = tf.data.Dataset.from_tensor_slices((X, Y)) \
                .batch(batch_size=batch_size, drop_remainder=True) \
                .shuffle(buffer_size=buffer_size)

    return dataset

train_generator = window_dataset(
    path_to_noisy_files=TRAIN_SET_NOISY,
    path_to_clean_files=TRAIN_SET_CLEAN,
    shift=sequence_shift,
    length=sequence_length
)

test_generator = window_dataset(
    path_to_noisy_files=TEST_SET_NOISY,
    path_to_clean_files=TEST_SET_CLEAN,
    shift=sequence_shift,
    length=sequence_length
)


# In[5]:


def RNN_model(sequence_length):
    """[summary]

    Args:
        sequence_length ([type]): [description]

    Returns:
        [type]: [description]
    """
    model = tf.keras.models.Sequential([
        tf.keras.layers.Lambda(lambda x: tf.expand_dims(x, axis=-1), input_shape=[None]),
        tf.keras.layers.SimpleRNN(sequence_length, return_sequences=True),
        tf.keras.layers.SimpleRNN(sequence_length),
        tf.keras.layers.Dense(1)])
    optimizer = tf.keras.optimizers.SGD(lr=1e-8, momentum=0.9)
    model.compile(loss=tf.keras.losses.Huber(), optimizer=optimizer, metrics=['mae'])
    return model


# In[6]:


model = RNN_model(sequence_length)
model.summary()


# In[9]:

tensorboard = tf.keras.callbacks.TensorBoard(
    log_dir='./logs'
)

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=3,
    min_delta=1e-5,
    restore_best_weights=True
)

checkpoints = tf.keras.callbacks.ModelCheckpoint(
    filepath='./checkpoints/1/weights.{epoch:02d}-{val_loss:.5f}.hdf5',
    save_weights_only=False,
    save_best_only=False
)

hist = model.fit(
    train_generator,
    validation_data=test_generator,
    steps_per_epoch=TRAINING_SET_SIZE,
    validation_steps=TEST_SET_SIZE,
    epochs=EPOCHS,
    callbacks=[tensorboard, early_stopping, checkpoints]
)
