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

## FUNCTIONS
def emField(charge, pos):
    if (pos - charge.pos).mag2 != 0:
        return (oofpez * charge.charge) / (pos - charge.pos).mag2 * (pos - charge.pos).norm();
    else:
        return vector(0, 0, 0)                                

def emForce(chargeA, chargeB):
    return emField(chargeA, chargeB.pos) * chargeB.charge

def updateMomentum(obj, force):
    obj.momentum += force * dt;

def getVelocity(obj):
    return obj.momentum / obj.mass;

def updatePosition(obj):
    obj.pos += getVelocity(obj) * dt;

## OBJECTS
objects = []
movingObjects = []

objectPositions = numpy.empty(num * 3, dtype = float)
thetas = numpy.linspace(0.0, 2.0 * pi, num)[0 : num - 1]

for theta in thetas:
    objects.append(sphere(pos=vector(cos(theta) * r, sin(theta) * r, 0), radius = .02, color=color.red, charge = q / num))

#cylinder(pos = vector(-l/2, 0, 0), axis = vector(l, 0, 0), radius = .02, opacity = 0.2)

#for x in range(int(-ceil(num / 2) + 1), int(ceil(num / 2))):
#    objects.append(sphere(pos=vector(x * l / num, 0, 0), radius = .01, color=color.red, charge = q / num))

movingObjects.append(sphere(pos=vector(0, 0, .2), radius = .1, color=color.blue,
        charge = qproton, momentum = vector(0,0,2e-16 * 0), mass = mproton, make_trail=True))

## CALCULATIONS
for theta1 in numpy.linspace(0.0, 2.0 * pi, aNum)[0:aNum - 1]:
    for theta2 in numpy.linspace(0.0, 2.0 * pi, bNum)[0:bNum - 1]:
        #for y in range(-2, 3):
        #for z in range(-2, 3): 
        pos = vector(cos(theta1) * r, sin(theta1) * r, 0) + vector(cos(theta2) * r / 8, 0, sin(theta2) * r / 8).rotate(theta1, vector(0, 0, 1))
        field = reduce(vector.__add__, map(lambda o: emField(o, pos), objects))
        arrow(pos = pos, axis = field / 5e4, color = color.orange)

while 1:
    for mo in movingObjects:
        for fo in objects: 
            updateMomentum(mo, emForce(fo, mo))
    for mo in movingObjects:
        updatePosition(mo)
    rate(5/dt)

