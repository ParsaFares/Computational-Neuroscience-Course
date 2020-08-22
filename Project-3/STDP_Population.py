from STDP_Neuron import STDP_Neuron
import random


class STDP_Population:
    def __init__(self, kind, pop_size, homo_neuron_data, relations, As, A_is_soft_bound, W_max, time_resolution, gamas=[1, 2], betas=[0.2, 0.3]):
        self.gamas = gamas
        self.betas = betas
        self.time_resolution = time_resolution
        self.pop_size = pop_size
        self.W_max = W_max
        self.W = [[0]*pop_size for _ in range(pop_size)]
        for i in range(pop_size):
            for j in range(pop_size):
                self.W[i][j] = relations[i][j]*70
        self.relations = relations
        self.As = As
        self.A_is_soft_bound = A_is_soft_bound
        self.neurons = []
        self.spike_matrix = [[0]*pop_size]*2

        for i in range(pop_size):
            manipulated_data = homo_neuron_data
            manipulated_data = [
                random.uniform(homo_neuron_data[0]-5, homo_neuron_data[0]+5),
                random.uniform(homo_neuron_data[1]-5, homo_neuron_data[1]+5),
                random.uniform(
                    max(homo_neuron_data[2]-3, 0), homo_neuron_data[2]+3),
                random.uniform(
                    max(homo_neuron_data[3]-3, 0), homo_neuron_data[3]+3),
                int(random.uniform(
                    max(homo_neuron_data[4]-5, 0), homo_neuron_data[4]+5)),
            ]
            self.neurons += [STDP_Neuron(kind[i],
                                         self.time_resolution, manipulated_data)]

    def do_STDP_cycle(self, time):
        for i in range(self.pop_size):
            self.neurons[i].do_STDP_cycle(time)
        self.extract_spike_matrix()
        self.update_W()

    def set_I(self, I):
        for i in range(self.pop_size):
            self.neurons[i].set_I(I[i]+100*self.calc_inside_activity(i))

    def extract_spike_matrix(self):
        spikes = []
        for i in range(self.pop_size):
            spikes += [self.neurons[i].is_spike()]
        self.spike_matrix += [spikes]

    def calc_inside_activity(self, neuron_index):
        sum = 0
        for i in range(self.pop_size):
            if self.relations[i][neuron_index] == 1:
                for j in range(1):
                    sum += self.spike_matrix[-j-1][i] * \
                        self.W[i][neuron_index] / (j+1)
        return sum

    def update_A(self):
        if not self.A_is_soft_bound:
            for i in range(self.pop_size):
                for j in range(self.pop_size):
                    if self.W[i][j] >= self.W_max or self.W[i][j] <= 0:
                        self.As[0][i][j] = 0
                        self.As[1][i][j] = 0
        else:
            for i in range(self.pop_size):
                for j in range(self.pop_size):
                    self.As[0][i][j] = max(0, self.gamas[0] *
                                           ((self.W_max - self.W[i][j])**self.betas[0]))
                    self.As[1][i][j] = max(0, self.gamas[1] *
                                           ((self.W_max - self.W[i][j])**self.betas[1]))

    def update_W(self):
        self.update_A()
        self.delta_W = []
        for i in range(self.pop_size):
            for j in range(self.pop_size):
                if self.relations[i][j] > 0:
                    self.delta_W += [self.time_resolution *
                                     (self.As[0][i][j] * self.neurons[i].get_x() * abs(self.spike_matrix[-1][j])
                                      - self.As[1][i][j] * self.neurons[j].get_x() * abs(self.spike_matrix[-1][i]))]
                    self.W[i][j] = min(
                        max(self.W[i][j] + self.delta_W[-1], 0), self.W_max)

    def get_delta_W(self):
        return self.delta_W

    def get_W(self):
        return self.W

    def get_pop_size(self):
        return self.pop_size
