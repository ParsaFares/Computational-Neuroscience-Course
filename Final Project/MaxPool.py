from tensorflow import keras
import tensorflow as tf
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import os


def maxpool_on_img(img, n, stride):
    p = keras.layers.MaxPooling2D(pool_size=(n, n), strides=(stride, stride))
    row_size = len(img)
    col_size = len(img[0])

    try:
        return np.array(p(tf.reshape(img, [1, row_size, col_size, 3])))[0]
    except:
        return np.array(p(tf.reshape(img, [1, row_size, col_size, 4])))[0]


def maxpool_on_all_dir(source_dir, distination_dir, n, stride):
    entries = os.listdir(source_dir)
    try:
        entries.remove(".DS_Store")
    except:
        pass

    for e in entries:
        img_files = os.listdir(source_dir+e+"/")
        for file_name in img_files:
            img = mpimg.imread(source_dir+e+"/"+file_name)
            try:
                os.mkdir(distination_dir+e)
            except:
                pass

            new_img = maxpool_on_img(img, n, stride)

            plt.imshow(new_img, cmap='gray')
            plt.imsave(distination_dir+e+"/" +
                       file_name, new_img, cmap="gray")
