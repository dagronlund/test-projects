__author__ = 'Fuckers'

import random

class Neuron():

    def __init__(self):
        self.a = 42
        print(self.a)

    def think(self):
        self.a = 43
        print('I don\' want to think: ' + str(self.a))

class Perceptron():

    def __init__(self, n):
        self.weights = []
        for i in range(n):
            self.weights[i] = random() * 2 - 1

    def think(self, values):
        for i in range(values):
            sum += self.weights[i] * values[i]
        return sum > 0


aNeuron = Neuron()
aNeuron.think()
