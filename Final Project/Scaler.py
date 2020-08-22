from skimage.transform import rescale
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import Converter
import numpy as np


def scale_img(img, scale):
    new_img = rescale(img, scale, anti_aliasing=False)

    return new_img


def scale_all_dir(source_dir, distination_dir, scales):
    entries = os.listdir(source_dir)
    try:
        entries.remove(".DS_Store")
    except:
        pass

    for file_name in entries:
        img = mpimg.imread(source_dir+file_name)
        img = np.array(Converter.convert_rgb_to_greyscale(img))

        for scale in scales:
            new_img = scale_img(img, scale)

            plt.imshow(np.array(new_img), cmap='gray')
            plt.imsave(distination_dir+str(scale)+"/"+file_name,
                       np.array(new_img), cmap="gray")
