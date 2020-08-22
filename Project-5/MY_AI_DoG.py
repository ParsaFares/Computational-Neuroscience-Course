def my_ai_min(cost_func, sigma1):
    sigma2 = 0.001
    while cost_func([sigma1, sigma2]) > 0.01:
        print(cost_func([sigma1, sigma2]), sigma2)
        sigma2 = round(sigma2 + 0.001, 3)
        if sigma2 == sigma1:
            sigma2 = round(sigma2 + 0.001, 3)

    return [sigma1, sigma2]
