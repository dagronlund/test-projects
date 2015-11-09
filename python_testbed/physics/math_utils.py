from math import *
from visual import vector, norm, mag
import numpy as np
import numpy.linalg as npl

def rotation_matrix(axis, theta):
    if mag(axis) == 0:
        return np.matrix(np.identity(3))
    axis = axis.norm()
    a = cos(theta / 2)
    b, c, d = -axis * sin(theta / 2)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.matrix([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
                      [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
                      [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])

def box_principal_axes(mass, width, height, depth):
    return (mass * (pow(height, 2.0) + pow(depth, 2.0)) / 12,
            mass * (pow(width, 2.0) + pow(depth, 2.0)) / 12, 
            mass * (pow(width, 2.0) + pow(height, 2.0)) / 12)

def dual_lines_principal_axes(mass, d1, d2, theta):
    x = mass * (pow(tan(theta), 2) / 3) * (pow(d1, 4) + pow(d2, 4)) / (d1 + d2)
    y = mass * (tan(theta) / 3) * pow((d1 + d2) / 2, 3)
    z = mass * (pow((d1 + d2) / cos(theta), 2) / 12 + pow((d1 - d2) / 2, 2) * pow(sin(theta), 2))
    return (x, y, z)

def cone_principal_axes(mass, radius, height):
    x = pow(radius, 2) + 4 * pow(height, 2)
    y = 2 * pow(radius, 2)
    z = pow(radius, 2) + 4 * pow(height, 2)
    return (3.0 / 20 * mass * x, 3.0 / 20 * mass * y, 3.0 / 20 * mass * z)

def delta_omega(principal_axes, omega, torque):
    i1, i2, i3 = principal_axes
    return vector(((i2 - i3) * omega.y * omega.z + torque.x) / i1,
                  ((i3 - i1) * omega.z * omega.x + torque.y) / i2,
                  ((i1 - i2) * omega.x * omega.y + torque.z) / i3)

def inertia_tensor(axes):
    return np.matrix([
        [axes[0], 0, 0],
        [0, axes[1], 0],
        [0, 0, axes[2]]])

def mtov(matrix):
    return vector(tuple(np.array(matrix).reshape(-1,).tolist()))