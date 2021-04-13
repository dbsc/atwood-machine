from manim import *
from manim.utils import paths
from numpy import sin, cos, sqrt, arccos
from scipy.integrate import odeint


def polar_to_cartesian(r, theta):
    return r * (RIGHT * cos(theta) + UP * sin(theta))


def cartesian_to_polar(vector):
    x, y, _ = vector
    r = sqrt(x**2 + y**2)
    if y >= 0:
        theta = arccos(x / r)
    else:
        theta = 2 * PI - arccos(x / r)
    return (r, theta)


class Mass(Circle):

    def __init__(self, mass, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mass = mass


class Pulley(Circle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AtwoodMachine(VGroup):
    gravity = 9.8
    friction = 0
    damping = 0
    separation = 4
    pulley_radius = 0.5
    string_style = {
        "stroke_width": 0.5 * DEFAULT_STROKE_WIDTH,
    }
    left_mass_config = {
        "radius": 0.3,
        "length": 3,
        "theta": 30 * DEGREES,
        "omega": 0,
        "mass": 1,
    }
    right_mass_config = {
        "radius": 0.3,
        "length": 4,
        "theta": 45 * DEGREES,
        "omega": 0,
        "mass": 1,
    }
    left_mass_style = {
        "stroke_color": BLUE,
    }
    right_mass_style = {
        "stroke_color": RED,
    }
    pulley_style = {
        "stroke_color": WHITE,
        "stroke_width": 1.5 * DEFAULT_STROKE_WIDTH
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.l1 = ValueTracker(self.left_mass_config["length"])
        self.l2 = ValueTracker(self.right_mass_config["length"])
        self.theta1 = ValueTracker(self.left_mass_config["theta"])
        self.theta2 = ValueTracker(self.right_mass_config["theta"])
        self.omega1 = ValueTracker(0) # has to be zero for now
        self.omega2 = ValueTracker(0) # has to be zero for now
        self.x = ValueTracker(0)
        self.v = ValueTracker(0) # has to be zero for now
        self.create_pulleys()
        self.create_masses()
        self.create_string()

    def create_fixed_center(self):
        self.fixed_center = VMobject()
        self.add(self.fixed_center)

    def create_masses(self):
        self.left_mass = Mass(mass=self.left_mass_config["mass"],
                                radius=self.left_mass_config["radius"]).move_to(
            self.get_left_mass_position()).set_style(**self.left_mass_style)
        self.right_mass = Mass(mass=self.right_mass_config["mass"],
                                 radius=self.right_mass_config["radius"]).move_to(
            self.get_right_mass_position()).set_style(**self.right_mass_style)
        self.add(self.left_mass, self.right_mass)

    def create_string(self):
        pass

    def create_pulleys(self):
        self.left_pulley = Pulley(radius=self.pulley_radius).move_to(
            self.separation / 2 * LEFT).set_style(**self.pulley_style)
        self.right_pulley = Pulley(radius=self.pulley_radius).move_to(
            self.separation / 2 * RIGHT).set_style(**self.pulley_style)
        self.add(self.left_pulley, self.right_pulley)

    def start_animation(self):
        pass

    def stop_animation(self):
        pass

    def get_left_mass_position(self):
        u = polar_to_cartesian(
            self.pulley_radius, PI - self.theta1.get_value()
        )
        v = polar_to_cartesian(
            self.l1.get_value(), 3 * PI / 2 - self.theta1.get_value()
        )
        return self.left_pulley.get_center() + u + v

    def get_right_mass_position(self):
        u = polar_to_cartesian(
            self.pulley_radius, self.theta2.get_value()
        )
        v = polar_to_cartesian(
            self.l2.get_value(), self.theta2.get_value() - PI / 2
        )
        return self.right_pulley.get_center() + u + v

    def diffeq_system(y, t, g, r, m1, m2, l1, l2):
        x, v, theta1, omega1, theta2, omega2 = y
        alfa1 = (omega1**2 * r - g * sin(theta1)) / l1
        alfa2 = (omega2**2 * r - g * sin(theta2)) / l2
        a = (m2 * (l2 * omega2**2 + g * cos(theta2)) -
             m1 * (l1 * omega1**2 + g * cos(theta1))) / (m1 + m2)
        return [v, a, omega1, alfa1, omega2, alfa2]

    def step_solve(self, dt):
        g, r = self.gravity, self.pulley_radius
        m1, m2 = self.left_mass.mass, self.right_mass.mass
        l1, l2 = self.l1.get_value(), self.l2.get_value()
        x, v = self.x.get_value(), self.v.get_value()
        theta1, omega1 = self.theta1.get_value(), self.omega1.get_value()
        theta2, omega2 = self.theta2.get_value(), self.omega2.get_value()
        y0 = [x, v, theta1, omega1, theta2, omega2]
        args = [g, r, m1, m2, l1, l2]
        t = [0, dt]
        return odeint(self.diffeq_system, y0, t, args)
