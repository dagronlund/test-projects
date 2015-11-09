import types
from visual import *
from visual.graph import *
import physics_utils

scene = display(width=800, height=600) # , range = 1)
gdisplay(x = 0, y = 0, width = 600, height = 400, 
    xmin = 0, xmax = 1e8, 
    ymin = -5e34, ymax = 5e34, 
    title = 'Spaceship Energy', xtitle = 't (s)', ytitle = 'Energy (J)',
    foreground = color.white, background = color.black)
k_curve = gcurve(color = color.yellow)
ug_curve = gcurve(color = color.cyan)
e_curve = gcurve(color = color.magenta)

dt = 1e5
# g = 6.674e-11
planet_scale = 100

sun_mass = 1.989e30
sun_radius = 696.3e6

earth_mass = 5.972e24
earth_velocity = 2.978589e4
earth_distance = 149.6e9
earth_radius = 6.371e6

moon_mass = 7.347673e22
moon_velocity = 1.022e3
moon_distance = 3.844e8
moon_radius = 1.73710e6

ship_mass = 170
#ship_distance = earth_radius + 1.846e5
ship_distance = earth_radius + 5e4
#ship_velocity = 7.793e3
ship_velocity = 1.3e4
ship_tli_dp = 3.15e3 * ship_mass

objects = []

sun = sphere(
    pos = vector(),
    momentum = vector(),
    mass = sun_mass,
    radius = sun_radius * 10,
    color = color.yellow,
    fixed = False,
    visible = True)

earth = sphere(
    pos = vector(earth_distance, 0, 0),
    #pos = vector(),
    momentum = vector(0, earth_velocity, 0) * earth_mass,
    #momentum = vector() * earth_mass,
    mass = earth_mass,
    radius = earth_radius * 1000,
    #radius = earth_radius,
    color = color.blue,
    fixed = False)

moon = sphere(
    pos = vector(moon_distance, 0, 0),
    momentum = vector(0, moon_velocity, 0) * moon_mass,
    mass = moon_mass,
    radius = moon_radius,
    color = color.white,
    fixed = True,
    visible = False)

ship = cylinder(
    pos = vector(ship_distance, 0, 0),
    momentum = vector(ship_velocity, 0, 0) * ship_mass,
    mass = ship_mass,
    radius = 2e6,
    axis = vector(5e6, 0, 0),
    color = color.red,
    make_trail = True,
    fixed = True,
    visible = False)

objects.append(sun)
objects.append(earth)
#objects.append(moon)
#objects.append(ship)

# Delta/V Key Listener
def keyInput(evt):
    if evt.key == ' ':
        tli_burn()
scene.bind('keydown', keyInput)

done = False
def tli_burn():
    global done, ship, dt
    if not done:
        ship.momentum += norm(ship.momentum) * ship_tli_dp
        dt *= 25
        print('TLI Burn')
        done = True

t = 0.0
while True:

    old_pos = vector(ship.pos)

    # Momentum and position update loops
    for o in objects:
        for other_o in objects:
            o.momentum += o.fg(other_o) * dt
    for o in objects:
        o.move(o.v() * dt)

    # Graph energy of objects
    k = 0
    ug = 0
    for o in objects:
        k += o.k()
        ug += o.ug(objects)

    k_curve.plot(pos = (t, k))
    ug_curve.plot(pos = (t, ug))
    e_curve.plot(pos = (t, k + ug))

    # Cosmetic scene fixes
    # ship.axis = norm(ship.v()) * 5e6

    # theta = atan2(norm(ship.pos).y, norm(ship.pos).x)
    # if theta < 0:
    #     theta = 2 * pi + theta
    # if theta > 1.17425 * pi:
    #     tli_burn()

    t += dt
    rate(60)
