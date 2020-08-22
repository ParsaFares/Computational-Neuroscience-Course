import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import os


def encode_img(img, k):
    new_images = [[[0]*len(img[0]) for _ in range(len(img))]
                  for _ in range(k)]

    s = 256 / k
    for i in range(len(img)):
        for j in range(len(img[0])):
            t = int(img[i][j][0]//s)
            new_images[t][i][j] = 255

    return new_images


def winner_take_all(images):
    for t in range(-1, len(images), -1):
        for i in range(len(images[t])):
            for j in range(len(images[t][0])):
                if images[t][i][j] != 0:
                    for r in range(-1, 2):
                        for c in range(-1, 2):
                            if i+r < 0 or j+c < 0 or i+r > len(images[t]) or j+c > len(images[t][0]):
                                break
                            if r != 0 or c != 0:
                                if images[t-1][i+r][j+c] != 0:
                                    images[t-2][i+r][j +
                                                     c] = images[t-1][i+r][j+c]
                                    images[t-1][i+r][j+c] = 0

    return images


def encode_all_in_dir(source_dir, distination_dir, k):
    entries = os.listdir(source_dir)
    try:
        entries.remove(".DS_Store")
    except:
        pass

    for e in entries:
        files = os.listdir(source_dir+e+"/")
        try:
            entries.remove(".DS_Store")
        except:
            pass

        try:
            os.mkdir(distination_dir+"/"+e)
        except:
            pass

        for f in files:
            img = mpimg.imread(source_dir+e+"/"+f)
            new_images = encode_img(img, k)
            new_images = winner_take_all(new_images)

            for i in range(k):
                plt.imshow(np.array(new_images[i]), cmap='gray')
                plt.imsave(distination_dir+e+"/"+str(i).zfill(3)+"_"+f,
                           np.array(new_images[i]), cmap="gray")
