# Magnetic Force on moving Proton in VPython

from __future__ import division
from visual import *
import numpy
scene.width = 800
scene.height = 600

## CONSTANTS
oofpez = 9e9   ## OneOverFourPiEpsilonZero
munofp = 1e-7 # MuNotOverFourPi
qproton = 1.6e-19
mproton = 1.67e-27
rproton = 0.8775e-15
fieldFactor = 2e-21
step = 4e-10

q = 2e-7
l = 1
r = 1
num = 200
aNum = 50
bNum = 16

# Helpful physics code wrapper
class PhysicsObject:

    def __init__(self, shape, pos=vector(), mass=0, velocity=vector(), charge=0):
        self.shape = shape
        self.pos = pos
        self.shape.pos = pos
        self.mass = mass
        self.momentum = velocity * mass
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

def magForce(charge, field): # f = qv x B
    return (charge.charge * charge.getVelocity()).cross(field)

def magDipoleField(moment, origin, pos):
    r = (pos - origin).mag
    if r != 0:
        r_hat = (pos - origin).norm()
        return (munofp) / pow(r, 3) * (3 * dot(moment, r_hat) * r_hat - moment) 
    else:
        return vector(0, 0, 0)

def safe_float_range(start, stop, steps):
    step = (stop - start) / steps
    for i in range(0, int(steps)):
        yield (start + i * step), step

def charge_in_ring():
    # Create lists of objects
    objects = []
    movingObjects = []

    # Create static objects
    for theta in numpy.linspace(0.0, 2.0 * pi, num)[0 : num - 1]:
        shape = sphere(radius = .02, color=color.red)
        objects.append(PhysicsObject(shape, pos=vector(cos(theta) * r, sin(theta) * r, 0), charge = q / num))
    
    # Create moving object
    shape = sphere(radius = .1, color=color.blue, make_trail=True)
    movingObjects.append(PhysicsObject(shape, pos=vector(0, 0, .2), charge = qproton, velocity = vector(0,0,0), mass = mproton))

    # Draw static arrows
    for theta1 in numpy.linspace(0.0, 2.0 * pi, aNum)[0:aNum - 1]:
        for theta2 in numpy.linspace(0.0, 2.0 * pi, bNum)[0:bNum - 1]:
            pos = vector(cos(theta1) * r, sin(theta1) * r, 0) + vector(cos(theta2) * r / 8, 0, sin(theta2) * r / 8).rotate(theta1, vector(0, 0, 1))
            field = reduce(vector.__add__, map(lambda o: emField(o, pos), objects))
            arrow(pos = pos, axis = field / 5e4, color = color.orange)

    return objects, movingObjects, 0.01

dipole_moment = vector(0, 20000, 0)
dipole_origin = vector(0, 0, 0)

def charge_in_mag_field():
    # Create lists of objects
    objects = []
    movingObjects = []

    # Create static objects
    for x, step in safe_float_range(-0.8, 0.8, 10):
        for z, step in safe_float_range(-0.8, 0.8, 10):
            arrow(pos=vector(x, 0, z), axis=vector(0, .2, 0), color=color.red)

    for x, step in safe_float_range(-0.8, 0.8, 10):
        for y, step in safe_float_range(-0.8, 0.8, 10):
            for z, step in safe_float_range(-0.8, 0.8, 10):
                pos = vector(x, y, z)
                axis = magDipoleField(dipole_moment, dipole_origin, pos)
                # axis_mag = axis.mag
                # axis = axis.norm() * math.log(axis_mag, 2)
                arrow(pos = pos, axis = axis, color=color.blue)

    # Create moving objects
    shape = sphere(radius = .01, color=color.blue, make_trail=True)
    movingObjects.append(PhysicsObject(shape, pos=vector(0, 0.2, 0),
            charge = qproton, velocity = vector(-2e6,1e6,0), mass = mproton))

    return objects, movingObjects, 1e-9

# Create object arrays
#objects, movingObjects = charge_in_ring()
objects, movingObjects, dt = charge_in_mag_field()

# Define constants
mag_field = vector(0.0, 0.2, 0.0)

# Simulation loop
while True:
    for mo in movingObjects:
        dipole_field = magDipoleField(dipole_moment, dipole_origin, mo.pos)
        mo.impulse(magForce(mo, dipole_field), dt)
    for mo in movingObjects:
        mo.move(dt)
    rate(30)
