from Neuron_Population import Population
import numpy as np
import random


class System():
    def __init__(self, pop_sizes, pop_kinds, has_external_current, pop_neuron_data, connectivity_probability, J):
        self.pops = []
        self.pop_kinds = pop_kinds
        self.pop_crowds = range(len(pop_sizes))
        self.pop_sizes = pop_sizes
        self.J = J
        self.has_external_current = has_external_current
        self.sys_data = []
        self.sys_time = []
        self.pops_activities = [[0]*len(pop_sizes)]
        self.mean = [70, 120, 0]
        for i in self.pop_crowds:
            self.pops += [Population(pop_sizes[i], pop_neuron_data[i],
                                     connectivity_probability[i][i], J[i][i])]

    def calc_and_set_outside_activity(self):
        self.pops_activities_setter()
        for i in self.pop_crowds:
            a = 0
            for j in self.pop_crowds:
                if j != i:
                    a += (self.pops_activities[-1][i]) * \
                        (self.J[i][j]/self.pop_sizes[j]) * self.pop_kinds[j]
            self.pops[i].set_outside_activity(a)

    def external_currents_setter(self, time):
        for i in self.pop_crowds:
            self.pops[i].set_external_current(self.currents[i][time])

    def random_I(self):
        y = 15
        N = 20  # increase for a smoother curve
        result = []
        time = int(self.sys_duration * 1000 * (1.0/self.time_resolution))
        x = np.linspace(0, time, time)
        for _ in x:
            # result += [20]
            # result += [y+10]
            # y += np.random.normal(scale=1)
            # y = random.uniform(10, 100)
            # y += random.uniform(-2, 2)
            result += [random.uniform(20, 60)]
        result = abs(np.convolve(result, np.ones((N,))/N)[(N-1):])

        return result

    def random_I_mean(self, i):
        result = []
        N = 40  # increase for a smoother curve
        time = int(self.sys_duration * 1000 * (1.0/self.time_resolution))
        x = np.linspace(0, time//2, time//2)
        for _ in x:
            result += [random.uniform(self.mean[i]-50, self.mean[i]+50)]
        for _ in x:
            result += [random.uniform(self.mean[1-i]-50, self.mean[1-i]+50)]

        result = abs(np.convolve(result, np.ones((N,))/N)[(N-1):])

        return result

    def calc_external_random_currents(self):
        self.currents = []
        for i in self.pop_crowds:
            rc = 0
            if self.has_external_current[i]:
                # rc = self.random_I()
                rc = self.random_I_mean(i)
            else:
                rc = [0]*int(self.sys_duration * 1000 *
                             (1.0/self.time_resolution))
            self.currents += [rc]

    def pops_activities_setter(self):
        pops_activities = []
        for i in self.pop_crowds:
            pops_activities += [sum(self.pops[i].get_activity())]
        self.pops_activities.append(pops_activities)

    def process_sys(self):
        self.calc_external_random_currents()
        for i in range(int(self.sys_duration * 1000 * (1.0/self.time_resolution))):
            self.calc_and_set_outside_activity()
            self.external_currents_setter(i)
            for j in self.pop_crowds:
                self.pops[j].do_cycle()
            self.update_sys_data(i)

    def set_time_resolution(self, time_resolution):
        self.time_resolution = time_resolution
        for pop in self.pops:
            pop.set_time_resolution(time_resolution)

    def set_sys_duration(self, duration):
        self.sys_duration = duration

    def get_sys_data(self):
        return self.currents, self.sys_data, self.sys_time, self.pops_activities

    def update_sys_data(self, t):
        t_spikes = []
        for i in self.pop_crowds:
            t_spikes += [e*t for e in self.pops[i].get_activity()]
        self.sys_time.append(t)
        self.sys_data.append(t_spikes)
