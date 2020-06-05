import numpy as np
import math
import matplotlib.pyplot as plt


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
        self.spike = 0
        self.spikes = []

    def set_exponential(self, sharpness):
        self.is_exponential = True
        self.sharpness = sharpness

    def set_adaptivity(self, ab_list, tau_list):
        self.adaptivity = True
        self.ab_list = ab_list
        self.w = [0] * len(ab_list)
        self.tau_list = tau_list

    def do_cycle(self):
        self.spikes += [self.spike]
        if self.remining_rest_time == 0:
            self.u_calc()
            return self.get_u(), self.get_I()
        else:
            self.remining_rest_time -= 1
            self.spike = 0  # False
            return self.get_u(), self.get_I()

    def u_calc(self):
        self.u = self.u - (self.time_resolution/(self.tau*100)) * \
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
                self.w[i] = self.w[i] + (self.time_resolution/self.tau_list[i]) * (self.ab_list[i][0] * (
                    self.u - self.u_rest) - self.w[i] + delta * self.ab_list[i][1]*self.tau_list[i])
            return sum(self.w)
        else:
            return 0

    def check_threshold(self):
        if self.u >= self.u_threshold:
            self.fire()

    def fire(self):
        self.spike = 1  # True
        self.remining_rest_time = self.reset_delay
        self.u = self.u_rest

    def set_I(self, I):
        self.I = I

    def get_u(self):
        return self.u

    def get_I(self):
        return self.I

    def is_spike(self):
        return self.spikes[-1]

    def set_time_resolution(self, time_resolution):
        self.time_resolution = time_resolution
