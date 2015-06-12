from time import sleep
from integration import *

# Velocity is m/s and Torque is Nm
tesla = [(0.0, 600.0), (18.8, 600.0), (22.4, 500.0), (24.6, 455.0), (26.8, 420.0), (29.1, 385.0), (32.6, 345.0),
         (35.8, 285.0), (38.0, 250.0), (40.2, 225.0), (42.5, 205.0), (44.7, 185.0), (46.9, 165.0), (49.2, 150.0),
         (58.1, 110.0)]




class Camaro:

	def __init__(self):
		self.velocity = 0
		self.position = 0

	def getAcceleration(self):
		return 1

	def simulate(self, dt):
		self.velocity += self.getAcceleration() * dt
		self.position += self.velocity * dt


class Tesla:

	def __init__(self):
		self.velocity = 0
		self.position = 0

	def getAcceleration(self, torgue):
		return (torgue * 9.71) / (0.2667 * 2239.0)

	def simulate(self, dt):
		self.velocity += self.getAcceleration() * dt
		self.position += self.velocity * dt


t = Tesla()
while True:
    t.simulate(.5)
    print(t.position)
    sleep(0.5)