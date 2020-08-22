def my_ai_min(cost_func, data):
    sigma = 0.001
    while cost_func(data) > 0.01:
        sigma = round(sigma + 0.001, 3)
        data[2] = sigma

    return data
