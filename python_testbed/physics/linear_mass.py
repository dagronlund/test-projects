from types import *
from visual import *
from visual.graph import * 
import physics_utils

display(width = 800, height = 600)
graph = gdisplay(x = 800, y = 0, width = 600, height = 400, xmin = 0,
    xmax = 20, ymin = 0, ymax = 1000, title = 'Position',
    xtitle = 't (s)', ytitle = 'Energy (J)',
    foreground = color.white, background = color.black)
k_curve = gcurve(color = color.yellow)
ug_curve = gcurve(color = color.cyan)
e_curve = gcurve(color = color.magenta)

dt = .002
dist = 5

def remove_normal(v, n):
    return v - v.proj(n)

m1 = sphere(radius = .25, mass = 10, make_trail = True, 
    momentum = vector(0, 0, -8.4 * 10),
    pos = vector(sin(pi / 3.0), -cos(pi / 3.0)) * dist)
arm = cylinder(pos = vector(), radius = .1)

t = 0
while True:
    # Update linear momentum
    m1.momentum = remove_normal(m1.momentum + m1.fgl() * dt, m1.pos)
    
    # Update linear position
    w = mag(m1.v() / dist)
    axis = norm(cross(m1.pos, m1.v()))
    arm.axis = m1.pos = m1.pos.rotate(w * dt, axis)

    # Graph the total energy of the system
    k_curve.plot(pos = (t, m1.k()))
    ug_curve.plot(pos = (t, m1.ugl(5)))
    e_curve.plot(pos = (t, m1.k() + m1.ugl(5)))
    
    # if t > 20:
    #     print(k + u)
    #     break
    t += dt
    rate(60)
