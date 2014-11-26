__author__ = 'Fuckers'


class Neuron():

    def __init__(self):
        self.a = 42
        print(self.a)

    def think(self):
        self.a = 43
        print('I don\' want to think: ' + str(self.a))


aNeuron = Neuron()
aNeuron.think()
