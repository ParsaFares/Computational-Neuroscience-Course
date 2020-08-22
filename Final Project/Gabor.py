import math
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import os
import numpy as np


def make_gabor_func(landa, theta, sigma, gamma):
    def gabor(X, Y):
        return math.exp(-(math.pow(X, 2)+math.pow(gamma*Y, 2))/(2*math.pow(sigma, 2)))*math.cos((2*math.pi*X/landa))

    def g_calc(x, y):
        X = x*math.cos(theta) + y*math.sin(theta)
        Y = -x*math.sin(theta) + y*math.cos(theta)
        return gabor(X, Y)

    return g_calc


def make_gabor_filter(n, gabor_func):
    m = [[0]*n for i in range(n)]
    h = n//2
    for i in range(n):
        for j in range(n):
            m[i][j] = round(100*gabor_func((i-h), (j-h)))

    return m


def dot_product_2d(m1, m2):
    s = 0
    for i in range(len(m1)):
        for j in range(len(m2)):
            s += m1[i][j][0] * m2[i][j]

    return 255-max(min(s/1000, 255), 0)


def apply_gabor_on_img(img, kernel):
    matrix = []
    period1 = len(img) - len(kernel) + 1
    period2 = len(img[0]) - len(kernel) + 1
    k = len(kernel)
    for i in range(period1):
        row = []
        for j in range(period2):
            m = [img[t][j:j+k] for t in range(i, i+k)]
            row.append(dot_product_2d(m, kernel))
        matrix.append(row)

    return matrix


def apply_gabor_on_dir(source_dir, distination_dir, kernel):
    entries = os.listdir(source_dir)
    try:
        entries.remove(".DS_Store")
    except:
        pass

    for file_name in entries:
        img = mpimg.imread(source_dir+file_name)
        try:
            if file_name[-4] == ".":
                dist_path = distination_dir+file_name[:-4]
                os.mkdir(dist_path)
            else:
                dist_path = distination_dir+file_name[:-5]
                os.mkdir(dist_path)
        except:
            pass

        for i in range(4):
            new_img = apply_gabor_on_img(img, kernel[i])

            plt.imshow(np.array(new_img), cmap='gray')
            plt.imsave(dist_path+"/"+str(i)+"_"+file_name,
                       np.array(new_img), cmap="gray")
