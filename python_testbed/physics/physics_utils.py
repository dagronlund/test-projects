from visual import vector, sphere

g = 6.674e-11
g_approx = 9.8

def move(self, delta):
	if not hasattr(self, 'fixed') or not self.fixed:
		self.pos += delta

def velocity(self):
    return self.momentum / self.mass

def g_force_approx(self):
    return self.mass * vector(0, -g_approx, 0)

def g_force(self, o):
	r = self.pos - o.pos
	if mag(r) > 0:
		return -norm(self.pos - o.pos) * g * self.mass * o.mass / mag2(self.pos - o.pos)
	return vector()

def ug_energy_approx(self, offset = 0):
	return self.mass * g_approx * (self.pos.y + offset)

def ug_energy(self, objects):
	ug = 0
	for o in objects:
		if self.pos != o.pos:
			ug += -g * self.mass * o.mass / mag(self.pos - o.pos)
	return ug

def kinetic_energy(self):
	return 0.5 * self.mass * mag2(self.v())

sphere.move = move
sphere.v = velocity
sphere.fgl = g_force_approx # Local force of gravity
sphere.fg = g_force
sphere.ugl = ug_energy_approx # Local gravitational potential
sphere.ug = ug_energy
sphere.k = kinetic_energy
