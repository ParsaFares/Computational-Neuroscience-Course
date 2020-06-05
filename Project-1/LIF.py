import numpy as np
import math
import matplotlib.pyplot as plt

time_resolution = 0.01  # ms


class Neuron:
    def __init__(self, u_rest, u_threshold, R, C, reset_delay):
        self.adaptivity = False
        self.ab_list = []
        self.w = []
        self.is_exponential = False
        self.sharpness = 0
        self.u_rest = u_rest
        self.u = u_rest
        self.reset_delay = reset_delay
        self.remining_rest_time = 0
        self.I = 0
        self.u_threshold = u_threshold
        self.R = R
        self.C = C
        self.tau = R * C

    def set_exponential(self, sharpness):
        self.is_exponential = True
        self.sharpness = sharpness

    def set_adaptivity(self, ab_list, tau_list):
        self.adaptivity = True
        self.ab_list = ab_list
        self.w = [0] * len(ab_list)
        self.tau_list = tau_list

    def do_cycle(self):
        if self.remining_rest_time == 0:
            self.u_calc()
            return self.get_u(), self.get_I()
        else:
            self.remining_rest_time -= 1
            return self.get_u(), self.get_I()

    def u_calc(self):
        self.u = self.u - (time_resolution/self.tau) * \
            (self.u + (self.R * self.adapt()) -
             self.exp() - self.u_rest - self.R * self.I)
        self.check_threshold()

    def exp(self):
        if self.is_exponential:
            return (self.sharpness * math.exp((self.u-self.u_threshold) / self.sharpness))
        else:
            return 0

    def adapt(self):
        if self.u >= self.u_threshold:
            delta = 1
        else:
            delta = 0
        if self.adaptivity:
            for i in range(len(self.w)):
                self.w[i] = self.w[i] + (time_resolution/self.tau_list[i]) * (self.ab_list[i][0] * (
                    self.u - self.u_rest) - self.w[i] + delta * self.ab_list[i][1]*self.tau_list[i])
            return sum(self.w)
        else:
            return 0

    def check_threshold(self):
        if self.u >= self.u_threshold:
            self.fire()

    def fire(self):
        self.remining_rest_time = self.reset_delay
        self.u = self.u_rest

    def set_I(self, I):
        self.I = I

    def get_u(self):
        return self.u

    def get_I(self):
        return self.I


class Neuron_Plotter:
    def __init__(self, neuron):
        self.neuron = neuron
        self.T = []  # time
        self.I = []  # current
        self.U = []  # potential

    def plot_UIT(self):
        plt.plot(self.T, self.U, self.T, self.I)
        plt.ylabel("potential/current")
        plt.xlabel("time")
        plt.show()

    def plot_FI(self):
        Is = np.linspace(0, 50, 51)
        f = 1.0 / (self.neuron.reset_delay + self.neuron.tau *
                   np.log((self.neuron.R * Is)/((self.neuron.R * Is) - (self.neuron.u_threshold-self.neuron.u_rest))))
        plt.plot(Is, f)
        plt.ylabel("f")
        plt.xlabel("current")
        plt.show()

    def set_plot_values(self, t):
        u, i = self.neuron.do_cycle()
        self.U += [u]
        self.I += [i]
        self.T += [t]

    def process_neuron(self, duration, is_current_random=False, current=[0]):
        self.duration = duration
        if is_current_random:
            I = self.random_I()
            for t in range(self.duration * 1000):
                self.neuron.set_I(I[t])
                self.set_plot_values(t)
        else:
            for t in range(self.duration * 1000):
                self.neuron.set_I(current[t//1000])
                self.set_plot_values(t)

    def random_I(self):
        y = 0
        N = 20  # increase for a smoother curve
        result = []
        x = np.linspace(0, self.duration * 1000, self.duration * 1000)
        for _ in x:
            result += [y]
            y += np.random.normal(scale=1)
        result = (np.convolve(result, np.ones((N,))/N)[(N-1):])
        return result


if __name__ == "__main__":
    time_resolution = 0.01  # ms
    my_neuron = Neuron(-10, 0, 2, 3, 10)
    my_neuron.set_exponential(10)
    my_neuron.set_adaptivity([[10, 20]], [10])
    neuron_plotter = Neuron_Plotter(my_neuron)
    neuron_plotter.process_neuron(duration=5, is_current_random=True)
    # neuron_plotter.process_neuron(
    #     duration=5, current=[50, 50, 50, 50, 50])
    # neuron_plotter.plot_FI()
    neuron_plotter.plot_UIT()
