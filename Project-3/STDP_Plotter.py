from STDP_Population import STDP_Population
import matplotlib.pyplot as plot
import random


class Plotter:
    def __init__(self, population):
        self.population = population
        self.dW = []
        self.dT = []

    def dW_dT_plotter(self, n):
        w = []
        t = []
        for i in range(len(self.dW)):
            if self.dW[i] != 0:
                w += [self.dW[i]]
                t += [self.dT[i]]

        plot.scatter(t, w, color='blue')
        plot.xlabel("time")
        plot.ylabel("weight")
        plot.savefig("./test/Fig_" + str(n) + ".png")
        plot.show()

    def collect_data(self):
        self.dW += self.population.get_delta_W()
        last_spikes = []
        pop_size = self.population.pop_size
        for i in range(pop_size):
            last_spikes += [self.population.neurons[i].get_last_spike()]
        for i in range(pop_size):
            for j in range(pop_size):
                if self.population.relations[i][j] > 0:
                    self.dT += [last_spikes[j] - last_spikes[i]]


if __name__ == "__main__":
    # Q1
     for j in range(10):
         pop = STDP_Population(["e", "e"], 2, [-70, -55, 5, 2, 3], [[0, 1], [0, 0]], [
             [[0.02, 0.02], [0.02, 0.02]], [[0.01, 0.01], [0.01, 0.01]]], True, 100, 1)
         plt = Plotter(pop)
         I = [[20, 100]]*5000

         for i in range(5000):
             pop.set_I(I[i])
             pop.do_STDP_cycle(i)
             plt.collect_data()

         plt.dW_dT_plotter(j+1)

     for j in range(20, 40):
         pop = STDP_Population(["e", "e"], 2, [-70, -55, 5, 2, 3], [[0, 1], [0, 0]], [
             [[0.02, 0.02], [0.02, 0.02]], [[0.01, 0.01], [0.01, 0.01]]], True, 100, 1)
         plt = Plotter(pop)
         I = [[100, 20]]*5000

         for i in range(5000):
             pop.set_I(I[i])
             pop.do_STDP_cycle(i)
             plt.collect_data()

         plt.dW_dT_plotter(j+1)
         print(pop.get_W())

    # Q2
    # def do_spike(n, size, I_spike):
    #     a = [0]*size
    #     a[n] = 0
    #     return a

    # rel = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    #        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    #        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    #        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    #        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    #        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    #        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    #        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    #        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    #        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    #        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    # size = 12
    # As = [[[20]*size for _ in range(size)]] + \
    #     [[[20]*size for _ in range(size)]]
    # pop = STDP_Population(["e"]*size, size, [-70, -55, 10, 4, 1],
    #                       rel, As, True, 100, 1)

    # patterns = []
    # patterns += [[1, 2, 3, 2, 2, 0, 0, 0, 0, 0]]
    # patterns += [[0, 0, 0, 0, 0, 2, 1, 2, 3, 1]]

    # I_spike = 100
    # pattern_frequency = 3
    # duration = 10
    # I_p = []
    # for p in patterns:
    #     I_p += [[[0]*pop.get_pop_size() for _ in range(max(p))]]

    #     for i in range(len(p)):
    #         if p[i] != 0:
    #             I_p[-1][p[i]-1][i] = I_spike*100

    # I = []
    # while(len(I) <= duration*1000):
    #     spikes = random.sample(range(10), pattern_frequency)
    #     for i in range(len(I_p)):
    #         I += I_p[i]
    #         for j in range(len(spikes)):
    #             I += [do_spike(spikes[j], pop.get_pop_size(), I_spike)]

    # plt = Plotter(pop)

    # for i in range(duration*1000):
    #     pop.set_I(I[i])
    #     pop.do_STDP_cycle(i)

    # for j in range(5):
    #     t = j * 10
    #     for i in range(len(I_p[0])):
    #         pop.set_I(I_p[0][i])
    #         pop.do_STDP_cycle(duration*1000+1+i+t)
    #     for i in range(2):
    #         pop.set_I([0]*12)
    #         pop.do_STDP_cycle(duration*1000+4+i+t)
    #     for i in range(len(I_p[1])):
    #         pop.set_I(I_p[1][i])
    #         pop.do_STDP_cycle(duration*1000+6+i+t)
    #     for i in range(2):
    #         pop.set_I([0]*12)
    #         pop.do_STDP_cycle(duration*1000+9+i+t)

    #     print("Round", j+1)
    #     # print(pop.spike_matrix[-20:])
    #     print(pop.spike_matrix[-6][-2], pop.spike_matrix[-6][-1])
    #     print(pop.spike_matrix[-1][-2], pop.spike_matrix[-1][-1])

    #     # print(pop.get_W())

    # Q3
#    def do_spike(n, size, I_spike):
#        a = [0]*size
#        a[n] = 0
#        return a
#
#    rel = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
#           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
#           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
#           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
#           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
#           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
#           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
#           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
#           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
#           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
#           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0]]
#    size = 13
#    As = [[[20]*size for _ in range(size)]] + \
#        [[[20]*size for _ in range(size)]]
#    pop = STDP_Population(["e"]*(size-1)+["i"], size, [-70, -55, 10, 7, 1],
#                          rel, As, True, 100, 1)
#
#    patterns = []
#    patterns += [[1, 2, 3, 2, 2, 0, 0, 0, 0, 0]]
#    patterns += [[0, 0, 0, 0, 0, 2, 1, 2, 3, 1]]
#
#    I_spike = 100
#    pattern_frequency = 4
#    duration = 15
#    I_p = []
#    for p in patterns:
#        I_p += [[[0]*pop.get_pop_size() for _ in range(max(p))]]
#
#        for i in range(len(p)):
#            if p[i] != 0:
#                I_p[-1][p[i]-1][i] = I_spike*100
#
#    I = []
#    while(len(I) <= duration*1000):
#        spikes = random.sample(range(10), pattern_frequency)
#        for i in range(len(I_p)):
#            I += I_p[i]
#            for j in range(len(spikes)):
#                I += [do_spike(spikes[j], pop.get_pop_size(), I_spike)]
#
#    plt = Plotter(pop)
#
#    for i in range(duration*1000):
#        pop.set_I(I[i])
#        pop.do_STDP_cycle(i)
#
#    r = 2
#    for j in range(6):
#        t = j * 10
#        for i in range(len(I_p[0])):
#            pop.set_I(I_p[0][i])
#            pop.do_STDP_cycle(duration*1000+1+i+t)
#        for i in range(r):
#            pop.set_I([0]*size)
#            pop.do_STDP_cycle(duration*1000+1+len(I_p[0])+i+t)
#        for i in range(len(I_p[1])):
#            pop.set_I(I_p[1][i])
#            pop.do_STDP_cycle(duration*1000+1+len(I_p[0])+r+i+t)
#        for i in range(r):
#            pop.set_I([0]*size)
#            pop.do_STDP_cycle(duration*1000+1+len(I_p[0])+r+r+i+t)
#
#        print("Round", j+1)
#        # print(pop.spike_matrix[-20:])
#        print(pop.spike_matrix[-2*r-2][-3], pop.spike_matrix[-6]
#              [-2], pop.spike_matrix[-6][-1])
#        print(pop.spike_matrix[-r+1][-3], pop.spike_matrix[-r+1]
#              [-2], pop.spike_matrix[-r+1][-1])
#
#        # print(pop.get_W())
