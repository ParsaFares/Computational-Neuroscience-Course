import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os


def make_img_square(img):
    row = len(img)
    col = len(img[0])

    if row > col:
        diff = row - col
        top = diff // 2
        bot = diff - top
        matrix = img[top:-bot]
    elif row < col:
        diff = col - row
        left = diff // 2
        right = diff - left
        matrix = [r[left:-right] for r in img]

    return matrix


def cut_img(img):
    h = len(img)
    w = len(img[0])

    return [img[t][w//4:3*w//4] for t in range(h//4, 3*h//4)]


def make_all_img_square(source_dir, distination_dir):
    entries = os.listdir(source_dir)
    entries.remove(".DS_Store")

    for file_name in entries:
        img = mpimg.imread(file_name)
        new_img = make_img_square(img)

        plt.imshow(new_img, cmap='gray')
        plt.imsave(distination_dir+"squared_"+file_name, new_img)
