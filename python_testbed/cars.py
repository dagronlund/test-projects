__author__ = 'dgronlund'

from time import sleep
from integration import *


def get_mph(velocity):
    return velocity * 2.2369362920544


def mph_to_ms(mph):
    return mph / 2.2369362920544


def g_to_ms2(g):
    return g * 9.81


# Velocity is m/s and Torque is Nm
tesla_data = [(0.0, 600.0), (18.8, 600.0), (22.4, 500.0), (24.6, 455.0), (26.8, 420.0), (29.1, 385.0), (32.6, 345.0),
         (35.8, 285.0), (38.0, 250.0), (40.2, 225.0), (42.5, 205.0), (44.7, 185.0), (46.9, 165.0), (49.2, 150.0),
         (58.1, 110.0)]


def interpolate(value, values):
    if value <= values[0][0]:  # If velocity is before range
        return values[0][1]  # Return minimum torque
    elif value >= values[-1][0]:  # If velocity is after range
        return values[-1][1]  # Return maximum torque
    for i in range(len(values) - 1):
        v1, t1 = values[i]
        v2, t2 = values[i + 1]
        if v1 <= value <= v2:  # Between v1 and v2
            ratio = (value - v1) / (v2 - v1)
            return t1 + (t2 - t1) * ratio  # Return interpolated torque


# Velocity is mph and acceleration g's
camaro_raw = [(0, .22), (20, .32), (25, .4), (30, .5), (35, .59), (40, .72), (45, .79), (50, .80), (55, .77), (60, .68),
    (65, .54), (70, .55), (75, .46), (80, .37), (85, .38), (90, .35), (95, .34), (100, .33), (105, .32), (110, .25),
    (115, .26), (120, .25), (125, .24)]

# Velocity in m/s and acceleration is m/s2
camaro_data = []
for v, a in camaro_raw:
    camaro_data.append((mph_to_ms(v), g_to_ms2(a)))


def get_tesla_acceleration(car):
    return (interpolate(car.velocity, tesla_data) * 9.71) / (0.2667 * 2239.0)


def get_camaro_acceleration(car):
    return interpolate(car.velocity, camaro_data) * 1.272


class Car:

    def __init__(self, acceleration):
        self.velocity = 0
        self.position = 0
        self.acceleration = acceleration

    def simulate(self, dt):
        self.velocity += self.acceleration(self) * dt
        self.position += self.velocity * dt


t = 0
car1 = Car(get_tesla_acceleration)
car2 = Car(get_camaro_acceleration)
while True:
    t += .5
    car1.simulate(.5)
    car2.simulate(.5)
    print("Time: ", t, ", Mph1: ", get_mph(car1.velocity), ", Mph2: ", get_mph(car2.velocity))
    sleep(0.5)

# Camaro Conversion: 1.272
