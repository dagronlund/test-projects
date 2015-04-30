__author__ = 'David'
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def float_range(start, stop, step, inclusive_list=False, include_end=False):
    i = start
    if not inclusive_list:
        stop -= step
    while i <= stop:
        yield i
        i += step
    if include_end:
        yield stop


def romberg_integral(f, a, b, method, accurate_digits=8, debug=False, adaptive=False):
    results = []
    if debug: print("Romberg Debug\n\t", end=" ")
    for iteration in range(0, math.ceil(accurate_digits / 2)):  # Each iteration gives about two more digits
        sub_results = []
        results.append(sub_results)
        for sub_iteration in range(0, iteration + 1):  # Each sub-iteration length is the iteration + 1
            if sub_iteration == 0:  # First sub-iteration value is the integration
                steps = math.pow(2, iteration)  # The first iteration is one step, second two steps, fours steps...
                if adaptive:
                    epsilon = (iteration + 1) * 2  # Rough estimate at accurate digits required in step
                    sub_results.append(adaptive_definite_integral(f, a, b, epsilon, method))
                else:
                    sub_results.append(definite_integral(f, a, b, steps, method))

                if debug: print(sub_results[-1], end=" ", flush=True)
            else:
                sub_results.append((math.pow(4, sub_iteration) * results[iteration][sub_iteration - 1] -
                    results[iteration - 1][sub_iteration - 1]) /
                    (math.pow(4, sub_iteration) - 1))  # The critical romberg code
                if debug: print(sub_results[-1], end=" ", flush=True)
        if debug: print('\n\t', end=" ")
    if debug: print()
    return results[-1][-1]  # In python -1 returns the last item, who knew?


def adaptive_definite_integral(f, a, b, epsilon, method):
    area = 0.0
    mid = (a + b) / 2
    guess = method(f, a, b - a)
    guess_a = method(f, a, mid - a)
    guess_b = method(f, mid, b - mid)
    if math.fabs(guess_a + guess_b - guess) > epsilon:
        return adaptive_definite_integral(f, a, mid, epsilon, method) + \
            adaptive_definite_integral(f, mid, b, epsilon, method)
    else:
        return guess_a + guess_b


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
#print("Rectangular: ", definite_integral(polynomial, 0.0, 1.0, 10, rect_estimate))
print("Trapezoidal: ", definite_integral(polynomial, 0.0, 1.0, 10, trap_estimate))
#print("Quadratic: ", definite_integral(polynomial, 0.0, 1.0, 10, quad_estimate))
print("Romberg: ", romberg_integral(polynomial, 0.0, 1.0, trap_estimate))
print()

print("Actual: ", 2)
#print("Rectangular: ", definite_integral(trig, 0.0, math.pi, 20, rect_estimate))
print("Trapezoidal: ", definite_integral(trig, 0.0, math.pi, 20, trap_estimate))
#print("Quadratic: ", definite_integral(trig, 0.0, math.pi, 20, quad_estimate))
print("Romberg: ", romberg_integral(trig, 0.0, math.pi, trap_estimate))
print()

print("Actual: ", math.log(2.0) - math.log(1.0))
print("Romberg: ", romberg_integral(lambda x: 1 / x, 1.0, 2.0, trap_estimate))
print()

print("Actual: ", math.sin(4.5 * math.pi) - math.sin(0.0))
print("Trapezoidal: ", definite_integral(lambda x: math.cos(x), 0.0, 4.5 * math.pi, 10, trap_estimate))
print("Adaptive: ", adaptive_definite_integral(lambda x: math.cos(x), 0.0, 4.5 * math.pi, .01, trap_estimate))
print("Romberg: ", romberg_integral(lambda x: math.cos(x), 0.0, 4.5 * math.pi, trap_estimate))
print("Adaptive Romberg: ", romberg_integral(lambda x: math.cos(x), 0.0, 4.5 * math.pi, trap_estimate, adaptive=True))
print()



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