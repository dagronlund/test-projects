__author__ = 'David'

from integration import *
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

print("Actual: ", 22.5)
print("Derivative: ", derivative(polynomial, 0.5))

print("Actual: ", 0.5)
run_trap_test(polynomial, 0.0, 1.0)

print("Actual: ", 2)
run_trap_test(trig, 0.0, math.pi)

print("Actual: ", math.log(2.0) - math.log(1.0))
run_trap_test(lambda x: 1 / x, 1.0, 2.0)

print("Actual: ", math.sin(4.5 * math.pi) - math.sin(0.0))
run_trap_test(lambda x: math.cos(x), 0.0, 4.5 * math.pi)

step = 0.01
a = 0.0
b = 1.0

xlist = []
ylist = []
for x in float_range(a, b, step, True, True):
    xlist.append(x)
    ylist.append(polynomial(x))
plt.plot(xlist, ylist)

axis = plt.gca()
for x in float_range(a, b, step, True, True):
    axis.add_patch(Rectangle((x, 0), step, polynomial(x + step / 2), facecolor="grey"))

plt.xlabel("X-Axis")
plt.ylabel("Y-Axis")
plt.show()
