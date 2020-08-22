import Gabor


def my_ai_min(cost_func, data):
    sigma = 0.001
    while cost_func(data) > 0.01:
        sigma = round(sigma + 0.001, 3)
        data[2] = sigma

    return data


def summation(n):
    def cost(data):
        my_gabor = Gabor.make_gabor_func(*data)
        matrix = Gabor.make_gabor_filter(n, my_gabor)
        s = 0
        for i in range(n):
            for j in range(n):
                s += abs(matrix[i][j])
        if s < 0.1:
            return 1000
        s = 0
        for i in range(n):
            for j in range(n):
                s += matrix[i][j]
        return abs(round(s, 2))
    return cost
