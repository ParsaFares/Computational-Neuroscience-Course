import math
from PIL import Image
from IPython.display import display
import os
import MY_AI_Gabor


def make_gabor(landa, theta, sigma, gamma):
    def gabor(X, Y):
        return math.exp(-(math.pow(X, 2)+math.pow(gamma*Y, 2))/(2*math.pow(sigma, 2)))*math.cos((2*math.pi*X/landa))

    def g_calc(x, y):
        X = x*math.cos(theta) + y*math.sin(theta)
        Y = -x*math.sin(theta) + y*math.cos(theta)
        return gabor(X, Y)

    return g_calc


def gabor_filter(n, gabor):
    m = [[0]*n for i in range(n)]
    h = n//2
    for i in range(n):
        for j in range(n):
            m[i][j] = round(100*gabor((i-h), (j-h)))

    return m


def print_matrix(m):
    for l in m:
        print(l)


def summation(m):
    def cost(data):
        my_gabor = make_gabor(*data)
        matrix = gabor_filter(m, my_gabor)
        s = 0
        for i in range(m):
            for j in range(m):
                s += abs(matrix[i][j])
        if s < 0.1:
            return 1000
        s = 0
        for i in range(m):
            for j in range(m):
                s += matrix[i][j]
        return abs(round(s, 2))
    return cost


def dot_product(m1, m2):
    s = 0
    for i in range(len(m1)):
        for j in range(len(m2)):
            try:
                s += m1[i][j] * (m2[i][j][0]+m2[i][j][1]+m2[i][j][2])/3
            except:
                s += m1[i][j] * m2[i][j]

    try:
        m2[0][0][0]
        return (round(s), round(s), round(s))
    except:
        return round(s)


if __name__ == "__main__":
    m = 5
    cost_func = summation(m)

    entries = os.listdir('images/')
    entries.remove(".DS_Store")

    for f in entries:
        Imported_Img = Image.open('images/'+f)
        pixels = Imported_Img.load()
        pixel_map = []
        for i in range(Imported_Img.size[0]):
            pixel_line = []
            for j in range(Imported_Img.size[1]):
                pixel_line += [pixels[i, j]]
            pixel_map += [pixel_line]

        data = []
        for a in range(4):
            data = [5, a*math.pi/4, 2, 5]
            data = MY_AI_Gabor.my_ai_min(cost_func, data)
            my_dog = make_gabor(*data)
            matrix = gabor_filter(m, my_dog)
            print_matrix(matrix)
            for i in range(m//2, Imported_Img.size[0]-m//2):
                for j in range(m//2, Imported_Img.size[1]-m//2):
                    sub_m = []
                    for t in range(m):
                        h = []
                        for k in range(m):
                            h += [pixel_map[i+t-m//2][j+k-m//2]]
                        sub_m += [h]

                    c = dot_product(matrix, sub_m)
                    pixels[i, j] = c

            display(Imported_Img)
            Imported_Img.show()
            Imported_Img.save("new images/new_"+str(m) +
                              "_gabor_"+str(a)+"*pi-quarter_"+f)
        Imported_Img.close()
