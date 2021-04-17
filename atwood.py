from mechanical_objects import AtwoodString, Mass, Pulley
from diffeq import atwood_diffeq_system
from polar import polar_to_cartesian
from scipy.integrate import odeint
from manim import *


class AtwoodMachine(VGroup):
    gravity = 9.8
    separation = 3
    pulley_radius = 0.2
    initial_string_velocity = 0
    string_style = {
        "stroke_width": 0.4 * DEFAULT_STROKE_WIDTH,
    }
    left_mass_config = {
        "radius": 0.1,
        "length": 2,
        "theta": 0,
        "omega": 0,
        "mass": 1,
    }
    right_mass_config = {
        "radius": 0.1,
        "length": 2,
        "theta": 0,
        "omega": 0,
        "mass": 1,
    }
    left_mass_style = {
        "stroke_color": BLUE,
        "stroke_width": 0.5 * DEFAULT_STROKE_WIDTH,
        "fill_color": BLUE,
        "fill_opacity": 1,
    }
    right_mass_style = {
        "stroke_color": RED,
        "stroke_width": 0.5 * DEFAULT_STROKE_WIDTH,
        "fill_color": RED,
        "fill_opacity": 1,
    }
    pulley_style = {
        "stroke_color": WHITE,
        "stroke_width": 0.25 * DEFAULT_STROKE_WIDTH,
    }
    VALID_PARAMETERS = [
        'gravity',
        'separation',
        'pulley_radius',
        'initial_string_velocity',
        'left_mass_style',
        'right_mass_style',
        'pulley_style',
    ]

    def __init__(self, **params):
        super().__init__()
        for key, value in params.items():
            if key in self.VALID_PARAMETERS:
                setattr(self, key, value)
        self.theta1 = ValueTracker(self.left_mass_config["theta"])
        self.theta2 = ValueTracker(self.right_mass_config["theta"])
        self.l1 = ValueTracker(self.left_mass_config["length"])
        self.l2 = ValueTracker(self.right_mass_config["length"])
        self.omega1 = self.left_mass_config["omega"]
        self.omega2 = self.right_mass_config["omega"]
        self.m1 = self.left_mass_config["mass"]
        self.m2 = self.right_mass_config["mass"]
        self.v = self.initial_string_velocity
        self.create_fixed_point()
        self.create_pulleys()
        self.create_masses()
        self.create_string()

    def create_fixed_point(self):
        self.fixed_point = VectorizedPoint()
        self.add(self.fixed_point)

    def create_masses(self):
        left_mass_radius = self.left_mass_config["radius"]
        right_mass_radius = self.right_mass_config["radius"]
        self.left_mass = Mass(radius=left_mass_radius).set_style(
            **self.left_mass_style)
        self.right_mass = Mass(radius=right_mass_radius).set_style(
            **self.right_mass_style)
        self.left_mass.get_center = self.get_left_mass_position
        self.right_mass.get_center = self.get_right_mass_position
        self.left_mass.add_updater(lambda m: m.move_to(m.get_center()))
        self.right_mass.add_updater(lambda m: m.move_to(m.get_center()))
        self.add(self.left_mass, self.right_mass)

    def create_string(self):
        self.string = AtwoodString(self)
        self.string.set_style(**self.string_style)
        self.add(self.string)

    def create_pulleys(self):
        self.left_pulley = Pulley(radius=self.pulley_radius, num=3, ratio=0.15).move_to(
            self.separation / 2 * LEFT).set_style(**self.pulley_style)
        self.right_pulley = Pulley(radius=self.pulley_radius, num=3, ratio=0.15).move_to(
            self.separation / 2 * RIGHT).set_style(**self.pulley_style)
        self.add(self.left_pulley, self.right_pulley)
        self.left_pulley.get_center = self.get_left_pulley_center
        self.right_pulley.get_center = self.get_right_pulley_center
        self.left_pulley.add_updater(left_pulley_updater(self))
        self.right_pulley.add_updater(right_pulley_updater(self))

    def start(self):
        self.left_pulley.clear_updaters()
        self.right_pulley.clear_updaters()
        self.add_updater(gravity_updater)

    def stop(self):
        self.remove_updater(gravity_updater)
        self.left_pulley.add_updater(left_pulley_updater(self))
        self.right_pulley.add_updater(right_pulley_updater(self))

    def step_solve(self, dt):
        g, r = self.gravity, self.pulley_radius
        m1, m2 = self.m1, self.m2
        l1, l2 = self.l1.get_value(), self.l2.get_value()

        x, v = 0, self.v
        theta1, omega1 = self.theta1.get_value(), self.omega1
        theta2, omega2 = self.theta2.get_value(), self.omega2

        y0 = (x, v, theta1, omega1, theta2, omega2)
        args = (g, r, m1, m2, l1, l2)
        t = [0, dt]

        return odeint(atwood_diffeq_system, y0, t, args=args)[1]

    def set_string_velocity(self, v):
        self.v = v

    def set_omega1(self, omega):
        self.omega1 = omega

    def set_omega2(self, omega):
        self.omega2 = omega

    def get_left_mass_position(self):
        u = polar_to_cartesian(self.pulley_radius, PI -
                               self.theta1.get_value())
        v = polar_to_cartesian(self.l1.get_value(), 3 *
                               PI / 2 - self.theta1.get_value())
        return self.get_left_pulley_center() + u + v

    def get_right_mass_position(self):
        u = polar_to_cartesian(self.pulley_radius, self.theta2.get_value())
        v = polar_to_cartesian(self.l2.get_value(),
                               self.theta2.get_value() - PI / 2)
        return self.get_right_pulley_center() + u + v

    def get_left_pulley_center(self):
        return self.fixed_center + LEFT * self.separation / 2

    def get_right_pulley_center(self):
        return self.fixed_center + RIGHT * self.separation / 2

    @property
    def fixed_center(self):
        return self.fixed_point.get_center()


def gravity_updater(m, dt):
    x, v, theta1, omega1, theta2, omega2 = m.step_solve(dt)
    l1 = m.l1.get_value() - x + m.pulley_radius * (theta1 - m.theta1.get_value())
    l2 = m.l2.get_value() + x + m.pulley_radius * (theta2 - m.theta2.get_value())

    m.set_string_velocity(v)
    m.theta1.set_value(theta1)
    m.set_omega1(omega1)
    m.theta2.set_value(theta2)
    m.set_omega2(omega2)

    m.l1.set_value(l1)
    m.l2.set_value(l2)
    m.left_pulley.rotate(-x / m.pulley_radius)
    m.right_pulley.rotate(-x / m.pulley_radius)


def left_pulley_updater(atwood):
    atwood.last_l1 = atwood.l1.get_value()
    atwood.last_theta1 = atwood.theta1.get_value()

    def updater(m):
        x = atwood.l1.get_value() - atwood.last_l1 - atwood.pulley_radius * (
            atwood.theta1.get_value() - atwood.last_theta1)
        m.rotate(x / atwood.pulley_radius)
        atwood.last_l1 = atwood.l1.get_value()
        atwood.last_theta1 = atwood.theta1.get_value()
    return updater


def right_pulley_updater(atwood):
    atwood.last_l2 = atwood.l2.get_value()
    atwood.last_theta2 = atwood.theta2.get_value()

    def updater(m):
        x = - atwood.l2.get_value() + atwood.last_l2 + atwood.pulley_radius * (
            atwood.theta2.get_value() - atwood.last_theta2)
        m.rotate(x / atwood.pulley_radius)
        atwood.last_l2 = atwood.l2.get_value()
        atwood.last_theta2 = atwood.theta2.get_value()
    return updater
