import random


def takeSecond(e):
    return e[1]


def calc_v(best, now):
    v1 = [best[0][0] - now[0][0], best[0][1] - now[0][1]]
    v2 = [now[2][0] - now[0][0], now[2][1] - now[0][1]]
    v = [v1[0] + v2[0], v1[1] + v2[1]]
    return v


def pso_min(cost_func):
    pop_cost = []
    for _ in range(1000):
        g = random.sample(range(1, 10), 2)
        pop_cost += [(g, cost_func(g), g)]
    pop_cost.sort(key=takeSecond)

    while(pop_cost[0][1] > 0.01):
        print(pop_cost[:2])
        g_best = pop_cost[0]

        new_pop = []
        for p in pop_cost:
            v = calc_v(g_best, p)
            new_p = [round(p[0][0]+v[0]/4+random.uniform(1, 10), 2),
                     round(p[0][1]+v[1]/4+random.uniform(1, 10), 2)]
            new_cost = cost_func(new_p)
            if new_cost < cost_func(p[2]):
                new_t = [(new_p, new_cost, new_p)]
            else:
                new_t = [(new_p, new_cost, p[2])]

            while new_t in new_pop:
                new_p = [round(new_p[0]+random.uniform(1, 10), 2),
                         round(new_p[1]+random.uniform(1, 10), 2)]
                new_cost = cost_func(new_p)
                if new_cost < cost_func(p[2]):
                    new_t = [(new_p, new_cost, new_p)]
                else:
                    new_t = [(new_p, new_cost, p[2])]

            new_pop += new_t

        pop_cost = new_pop
        pop_cost.sort(key=takeSecond)

    return pop_cost[0][0]
