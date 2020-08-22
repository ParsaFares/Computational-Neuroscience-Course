import math
from LIF_Neuron import Neuron


class STDP_Neuron(Neuron):
    def __init__(self, kind, time_resolution, homo_neuron_data):
        self.I = 0
        self.x = 0
        Neuron.__init__(self, kind, *homo_neuron_data[:5])
        self.set_time_resolution(time_resolution)
        self.last_spike = -1

    def do_STDP_cycle(self, time):
        self.set_I(self.I)
        self.do_cycle()
        if self.is_spike() != 0:
            self.last_spike = time
        self.update_x()

    def update_x(self):
        self.x = self.x - self.time_resolution * \
            (self.x/self.tau - abs(self.is_spike()))

    def get_x(self):
        return self.x

    def get_last_spike(self):
        return self.last_spike
