# Magnetic Force on moving Proton in VPython

from __future__ import division
from visual import *
import numpy
scene.width = 800
scene.height = 600

## CONSTANTS
oofpez = 9e9   ## OneOverFourPiEpsilonZero
qproton = -1.6e-19
mproton = 1.7e-14
rproton = 0.8775e-15
fieldFactor = 2e-21
step = 4e-10
dt = .01

q = 2e-7
l = 1
r = 1
num = 200
aNum = 50
bNum = 16

# Helpful physics code wrapper
class PhysicsObject:

    def __init__(self, shape, pos=vector(), mass=0, momentum=vector(), charge=0):
        self.shape = shape
        self.pos = pos
        self.shape.pos = pos
        self.mass = mass
        self.momentum = momentum
        self.charge = charge

    def getVelocity(self):
        return self.momentum / self.mass

    def impulse(self, f, dt):
        self.momentum += f * dt

    def move(self, dt):
        self.pos += self.getVelocity() * dt
        self.shape.pos = self.pos

# Utility functions
def emField(charge, pos):
    if (pos - charge.pos).mag2 != 0:
        return (oofpez * charge.charge) / (pos - charge.pos).mag2 * (pos - charge.pos).norm()
    else:
        return vector(0, 0, 0)                                

def emForce(chargeA, chargeB):
    return emField(chargeA, chargeB.pos) * chargeB.charge

# Create object arrays
objects = []
movingObjects = []

# Create static objects
for theta in numpy.linspace(0.0, 2.0 * pi, num)[0 : num - 1]:
    shape = sphere(radius = .02, color=color.red)
    objects.append(PhysicsObject(shape, pos=vector(cos(theta) * r, sin(theta) * r, 0), charge = q / num))

# Create moving object
shape = sphere(radius = .1, color=color.blue, make_trail=True)
movingObjects.append(PhysicsObject(shape, pos=vector(0, 0, .2), charge = qproton, momentum = vector(0,0,2e-16 * 0), mass = mproton))

# Draw static arrows
for theta1 in numpy.linspace(0.0, 2.0 * pi, aNum)[0:aNum - 1]:
    for theta2 in numpy.linspace(0.0, 2.0 * pi, bNum)[0:bNum - 1]:
        pos = vector(cos(theta1) * r, sin(theta1) * r, 0) + vector(cos(theta2) * r / 8, 0, sin(theta2) * r / 8).rotate(theta1, vector(0, 0, 1))
        field = reduce(vector.__add__, map(lambda o: emField(o, pos), objects))
        arrow(pos = pos, axis = field / 5e4, color = color.orange)

# Simulation loop
while 1:
    for mo in movingObjects:
        for fo in objects:
            mo.impulse(emForce(fo, mo), dt)
    for mo in movingObjects:
        mo.move(dt)
    rate(5/dt)

