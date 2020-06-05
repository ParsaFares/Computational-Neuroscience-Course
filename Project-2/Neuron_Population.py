from LIF_Neuron import Neuron
import random


class Population():
    def __init__(self, pop_size, homo_neuron_data, connectivity_probability, J):
        self.neurons = []
        self.neuron_neighborhood = []
        self.crowd = range(pop_size)
        self.spike_matrix = [[0]*pop_size]+[[0]*pop_size]
        if connectivity_probability != 0:
            self.W = J / (pop_size*connectivity_probability)
        else:
            self.W = 0
        for _ in self.crowd:
            # homo_neuron_data = [u_rest, u_threshold, R, C, reset_delay, sharpness, ab_list, tau_list]
            manipulated_data = [
                random.uniform(homo_neuron_data[0]-5, homo_neuron_data[0]+5),
                random.uniform(homo_neuron_data[1]-5, homo_neuron_data[1]+5),
                random.uniform(
                    max(homo_neuron_data[2]-3, 0), homo_neuron_data[2]+3),
                random.uniform(
                    max(homo_neuron_data[3]-3, 0), homo_neuron_data[3]+3),
                int(random.uniform(
                    max(homo_neuron_data[4]-5, 0), homo_neuron_data[4]+5)),
                random.uniform(
                    max(homo_neuron_data[5]-3, 0), homo_neuron_data[5]+3),
            ]
            neuron = Neuron(*manipulated_data[:5])
            neuron.set_exponential(manipulated_data[-1])
            neuron.set_adaptivity(*homo_neuron_data[-2:])
            self.neurons += [neuron]
            self.neuron_neighborhood += [random.sample(
                self.crowd, k=int(len(self.crowd) * connectivity_probability))]

    def set_outside_activity(self, activity):
        self.outside_activity = activity

    def set_external_current(self, current):
        self.external_current = current

    def calc_inside_activity(self):
        self.inside_activity = []
        for neuron in self.neuron_neighborhood:
            spikes = 0
            for neighbor in neuron:
                spikes += self.spike_matrix[-1][neighbor] + \
                    self.spike_matrix[-2][neighbor]
            self.inside_activity += [spikes]

    def calc_and_set_current(self):
        for i in range(len(self.neurons)):
            I = self.outside_activity + \
                self.external_current + self.inside_activity[i] * self.W
            self.neurons[i].set_I(I)

    def do_cycle(self):
        self.calc_inside_activity()
        self.calc_and_set_current()
        for i in self.crowd:
            self.neurons[i].do_cycle()
        self.calc_pop_spikes()

    def calc_pop_spikes(self):
        spike_array = []
        for i in self.crowd:
            spike_array += [self.neurons[i].is_spike()]
        self.spike_matrix += [spike_array]

    def get_activity(self):
        return self.spike_matrix[-1]

    def set_time_resolution(self, time_resolution):
        self.time_resolution = time_resolution
        for neuron in self.neurons:
            neuron.set_time_resolution(time_resolution)
