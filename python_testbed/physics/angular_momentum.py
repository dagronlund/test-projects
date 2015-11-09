from visual import *
import numpy as np
import numpy.linalg as npl
from math_utils import *
from physics_utils import *

def orient_box(box, sys):
    box.axis = mtov(sys[:,0]) * box.size.x
    box.up = mtov(sys[:,1]) * box.size.y

def orient_rods(rods, sys):
    for rod in rods:
        rod.pos = mtov(np.dot(sys, rod.p))
        rod.axis = mtov(np.dot(sys, rod.a))

def orient_cone(cone, sys):
    cone.pos = sys[:,1] * cone.height / 2.0
    cone.axis = -sys[:,1] * cone.height

display(width = 800, height = 600)

dt = 0.005
sys = np.matrix(np.identity(3))
omega_p = vector(3, .01, 0)

theta = pi / 8
d1 = 6
d2 = .1
m = 5

b = box(size = (6, 10, 2), color = color.red, mass = 5, opacity = 0.5)
axes = box_principal_axes(b.mass, b.size.x, b.size.y, b.size.z)

# c1 = cylinder(p = vector(-(d1 + d2) / 2, 0, 0),
#               a = vector(d1, d1 * tan(theta), 0),
#               radius = .1)
# c2 = cylinder(p = vector(-(d1 + d2) / 2, 0, 0),
#               a = vector(d1, -d1 * tan(theta), 0),
#               radius = .1)
# c3 = cylinder(p = vector(-(d1 + d2) / 2, 0, 0),
#               a = vector(-d2, d2 * tan(theta), 0),
#               radius = .1)
# c4 = cylinder(p = vector(-(d1 + d2) / 2, 0, 0),
#               a = vector(-d2, -d2 * tan(theta), 0),
#               radius = .1)
# parts = [c1, c2, c3, c4]
# axes = dual_lines_principal_axes(m, d1, d2, theta)

# top = cone(radius = 2.5, height = 5, color = color.blue)
# axes = cone_principal_axes(m, 2.5, 5)

omega_axis = arrow(pos = vector(-8, -8, -8), shaftwidth = 0, 
    color = color.yellow, opacity = 1)
l_axis = arrow(pos = vector(-8, -10, -8), shaftwidth = 0, 
    color = color.green, opacity = 1)
box_axis = arrow(color = color.orange, shaftwidth = 0)
# cone_axis = arrow(color = color.orange, shaftwidth = 0, make_trail = True)
# x_axis = arrow(color = color.magenta)
# y_axis = arrow(color = color.yellow)
# z_axis = arrow(color = color.cyan)

while True:
    # Convert omega-prime to omega
    omega = mtov(np.dot(sys.I, omega_p))
    
    # Update omega from Euler's equations
    omega += delta_omega(axes, omega, vector()) * dt
    
    # Calculate l-prime from omega
    l = mtov(np.dot(sys, mtov(np.dot(inertia_tensor(axes), omega))))
    
    # Convert omega back to omega-prime
    omega_p = mtov(np.dot(sys, omega))

    # Rotate coordinate system by omega-prime
    sys = np.dot(rotation_matrix(norm(omega_p), mag(omega_p) * dt), sys)

    # Rotate object to match coordinate system
    orient_box(b, sys)
    # orient_rods(parts, sys)
    # orient_cone(top, sys)

    # Update diagnostics
    omega_axis.axis = norm(omega_p) * 4
    l_axis.axis = norm(l) * 4
    # cone_axis.pos = -top.axis * 0.75
    # cone_axis.axis = top.axis * 0.75
    box_axis.axis = mtov(sys[:,0]) * b.size.x / 2.0
    # x_axis.axis = mtov(sys[:,0])
    # y_axis.axis = mtov(sys[:,1])
    # z_axis.axis = mtov(sys[:,2])
    # print(l.mag)

    rate(180)
