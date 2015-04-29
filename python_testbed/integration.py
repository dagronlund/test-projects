__author__ = 'David'
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def float_range(start, stop, step, inclusive_list=False, include_end=False):
    i = start
    if not inclusive_list:
        stop -= step
    while i < stop:
        yield i
        i += step
    if include_end:
        yield stop


def definite_integral(f, a, b, steps, method):
    area = 0.0
    step = (b - a) / steps
    for x in float_range(a, b, step):
        area += method(f, x, step)
    return area


def rect_estimate(f, x, step):
    return f(x + step / 2) * step


def trap_estimate(f, x, step):
    return (f(x) + f(x + step)) * step / 2


def quad_estimate(f, x, step):
    return (step / 6) * (f(x) + 4 * f(x + step / 2) + f(x + step))


def polynomial(x):
    return 1200 * x ** 5 - 3060 * x ** 4 + 2730 * x ** 3 - 990 * x ** 2 + 120 * x


def trig(x):
    return math.sin(x)


print("Actual: ", 0.5)
print("Rectangular: ", definite_integral(polynomial, 0.0, 1.0, 10, rect_estimate))
print("Trapezoidal: ", definite_integral(polynomial, 0.0, 1.0, 10, trap_estimate))
print("Quadratic: ", definite_integral(polynomial, 0.0, 1.0, 10, quad_estimate))

print("Actual: ", 2)
print("Rectangular: ", definite_integral(trig, 0.0, math.pi, 20, rect_estimate))
print("Trapezoidal: ", definite_integral(trig, 0.0, math.pi, 20, trap_estimate))
print("Quadratic: ", definite_integral(trig, 0.0, math.pi, 20, quad_estimate))

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