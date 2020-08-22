from Neural_System import System
import numpy as np
import math
import matplotlib.pyplot as plt


class Sys_Plotter():
    def __init__(self, sys):
        self.sys = sys

    def set_sys_data(self):
        self.I, self.raw_data, self.time, self.activities = self.sys.get_sys_data()

    def plot_raster(self):
        self.raw_data = np.transpose(self.raw_data)
        manipulated_data = []
        for n in self.raw_data:
            manipulated_data.append([d for d in n if d != 0])
        plt.eventplot(manipulated_data, color=self.colors,
                      linewidths=2,
                      linelengths=2,
                      lineoffsets=2)
        plt.ylabel("neurons")
        plt.xlabel("time")
        plt.show()

    def plot_AT(self):
        activities = np.transpose(self.activities)
        plt.plot(self.time, activities[0][1:], self.time,
                 activities[1][1:], self.time, activities[2][1:])
        plt.ylabel("activities")
        plt.xlabel("time")
        plt.show()

    def plot_IT(self):
        plt.plot(self.time, self.I[0], self.time, self.I[1])
        plt.ylabel("current")
        plt.xlabel("time")
        plt.show()

    def set_color(self, colors):
        self.colors = colors


if __name__ == "__main__":
    # Q1
    # pop_sizes = [800, 200]
    # pop_kinds = [1, -1]
    # has_external_input = [True, True]
    # neuron_datas = [[-70, -55, 3, 4, 10, 10, [[10, 2]], [10]],
    #                 [-70, -50, 2, 5, 10, 2, [[1, 20]], [10]]]
    # connectivity_probability = [[0.1, 1], [1, 0]]
    # J = [[100, 10], [100, 0]]
    # sys = System(pop_sizes, pop_kinds, has_external_input,
    #              neuron_datas, connectivity_probability, J)
    # sys.set_sys_duration(5)
    # sys.set_time_resolution(1)
    # sys.process_sys()
    # plotter = Sys_Plotter(sys)
    # plotter.set_sys_data()
    # plotter.set_color([[0, 0, 1]]*pop_sizes[0] + [[1, 0, 0]]*pop_sizes[1])
    # plotter.plot_raster()
    # plotter.plot_IT()

    # # Q2
    pop_sizes = [200, 200, 100]
    pop_kinds = [1, 1, -1]
    has_external_input = [True, True, False]
    neuron_datas = [[-70, -55, 3, 4, 10, 10, [[10, 22]], [20]],
                    [-70, -55, 3, 4, 10, 10, [[10, 22]], [20]],
                    [-70, -65, 3, 4, 10, 10, [[10, 22]], [20]]]
    connectivity_probability = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    J = [[200, 0, 100], [0, 200, 100], [100, 100, 0]]
    sys = System(pop_sizes, pop_kinds, has_external_input,
                 neuron_datas, connectivity_probability, J)
    sys.set_sys_duration(5)
    sys.set_time_resolution(1)
    sys.process_sys()
    plotter = Sys_Plotter(sys)
    plotter.set_sys_data()
    plotter.set_color([[0, 0, 1]]*pop_sizes[0] + [[0, 1, 0]]
                      * pop_sizes[1] + [[1, 0, 0]]*pop_sizes[2])
    plotter.plot_raster()
    plotter.plot_IT()
    plotter.plot_AT()
