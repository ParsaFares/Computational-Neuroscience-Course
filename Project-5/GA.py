import random
import math


def mutation1(a):
    t = min(a[0], a[1])
    return [a[0]-t/2, a[1]-t/2]


def mutation2(a):
    return [round(math.sqrt(a[0])/2, 2), round(math.sqrt(a[1])/2, 2)]


def crossing(a, b):
    return [round((a[0]+b[0])/2, 2), round((a[1]+b[1])/2, 2)]


def takeSecond(e):
    return e[1]


def ga_min(cost_func):
    pop_cost = []
    for i in range(1000):
        g = random.sample(range(1, 20), 2)
        pop_cost += [(g, cost_func(g))]
    pop_cost.sort(key=takeSecond)

    while(pop_cost[0][1] > 0.01):
        print(pop_cost[:2])
        mutate = random.sample(pop_cost, 100)
        cross = random.sample(pop_cost, 100)

        for m in mutate[:50]:
            g = mutation1(m[0])
            pop_cost += [(g, cost_func(g))]
        for m in mutate[50:]:
            g = mutation2(m[0])
            pop_cost += [(g, cost_func(g))]

        for i in range(0, 100, 2):
            g = crossing(cross[i][0], cross[-i-1][0])
            pop_cost += [(g, cost_func(g))]

        for i in range(100):
            g = random.sample(range(1, 20), 2)
            pop_cost += [(g, cost_func(g))]

        pop_cost.sort(key=takeSecond)
        new_pop = []
        for i in pop_cost:
            if i not in new_pop:
                new_pop += [i]
        pop_cost = new_pop
        pop_cost = pop_cost[:100]

    return pop_cost[0][0]
