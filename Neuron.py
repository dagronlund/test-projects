__author__ = 'Ethan'

import random

class Neuron():

    def __init__(self, num_inputs):
        self.weights = []
        self.values = [];
        for i in range(num_inputs):
            self.weights[i] = random() * 2 - 1

    def update(self, values):
        for i in range(values):
            sum += self.weights[i] * values[i]
        return sum > 0