import math
from PIL import Image
from IPython.display import display
# import GA
# import PSO
import MY_AI_DoG
import os


def make_dog(sigma1, sigma2):
    def gaussian(sigma, s):
        return (1/(sigma*math.sqrt(2*math.pi)))*(math.exp(-(s)/(2*math.pow(sigma, 2))))

    def g_calc(x, y):
        return gaussian(sigma1, math.pow(x, 2)+math.pow(y, 2)) - gaussian(sigma2, math.pow(x, 2)+math.pow(y, 2))

    return g_calc


def dog_filter(n, dog):
    m = [[0]*n for i in range(n)]
    h = n//2
    for i in range(n):
        for j in range(n):
            m[i][j] = -round(100*dog((i-h)/2, (j-h)/2))

    return m


def print_matrix(m):
    for l in m:
        print(l)


def summation(m):
    def cost(ss):
        if ss[0] == ss[1]:
            return 1000
        if ss[0] == 0 or ss[1] == 0:
            return 1000
        my_dog = make_dog(ss[0], ss[1])
        matrix = dog_filter(m, my_dog)
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
    m = 3
    k = 3
    # ss = GA.ga_min(summation(m))
    # ss = PSO.pso_min(summation(m))
    ss = MY_AI_DoG.my_ai_min(summation(m), 0.22)
    my_dog = make_dog(ss[0], ss[1])
    matrix = dog_filter(m, my_dog)
    s = 0
    for i in range(m):
        for j in range(m):
            s += matrix[i][j]

    print(ss)
    print_matrix(matrix)
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
        Imported_Img.save("new images/new_"+str(m)+"_dog_"+f)
        Imported_Img.close()

        Imported_Img = Image.open('new images/new_'+str(m)+'_dog_'+f)
        pixels = Imported_Img.load()

        pixel_map = []
        for i in range(Imported_Img.size[0]):
            pixel_line = []
            for j in range(Imported_Img.size[1]):
                pixel_line += [pixels[i, j]]
            pixel_map += [pixel_line]

        for t in range(k):
            for i in range(Imported_Img.size[0]):
                for j in range(Imported_Img.size[1]):
                    try:
                        pixel_map[0][0][0]
                        if pixel_map[i][j][0] <= (255//k)*(t+1) and pixel_map[i][j][0] > (255//k)*(t):
                            pixels[i, j] = pixel_map[i][j]
                        else:
                            pixels[i, j] = (255, 255, 255)
                    except:
                        if pixel_map[i][j] <= (255//k)*(t+1) and pixel_map[i][j] > (255//k)*(t):
                            pixels[i, j] = pixel_map[i][j]
                        else:
                            pixels[i, j] = 255

            display(Imported_Img)
            Imported_Img.show()
            Imported_Img.save("new images/new_"+str(m)+"_dog_"+str(t+1)+"_"+f)
