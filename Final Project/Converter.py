import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import numpy as np


def convert_rgb_to_greyscale(img):
    new_img = []
    for r in img:
        row = []
        for c in r:
            # New grayscale image = ( (0.3 * R) + (0.59 * G) + (0.11 * B) )
            row.append(c[0]*0.3+c[1]*0.59+c[2]*0.11)
        new_img.append(row)

    return new_img


def convert_all_in_dir(source_dir, distination_dir):
    entries = os.listdir(source_dir)
    entries.remove(".DS_Store")

    for file_name in entries:
        img = mpimg.imread(source_dir+file_name)
        new_img = convert_rgb_to_greyscale(img)

        plt.imshow(np.array(new_img), cmap='gray')
        plt.imsave(distination_dir+file_name,
                   np.array(new_img), cmap="gray")
