from mechanical_objects import AtwoodString, Mass, Pulley
from diffeq import atwood_diffeq_system
from misc import polar_to_cartesian
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theta1 = ValueTracker(self.left_mass_config["theta"])
        self.theta2 = ValueTracker(self.right_mass_config["theta"])
        self.l1 = ValueTracker(self.left_mass_config["length"])
        self.l2 = ValueTracker(self.right_mass_config["length"])

        self.omega1 = self.left_mass_config["omega"]
        self.omega2 = self.right_mass_config["omega"]
        self.m1 = self.left_mass_config["mass"]
        self.m2 = self.right_mass_config["mass"]
        self.v = self.initial_string_velocity

        self._create_midpoint()
        self._create_pulleys()
        self._create_masses()
        self._create_string()

    def _create_midpoint(self):
        self.midpoint = VectorizedPoint()
        self.add(self.midpoint)

    def _create_masses(self):
        r1 = self.left_mass_config["radius"]
        r2 = self.right_mass_config["radius"]

        self.left_mass = Mass(radius=r1).set_style(**self.left_mass_style)
        self.right_mass = Mass(radius=r2).set_style(**self.right_mass_style)

        self.left_mass.add_updater(
            lambda m: m.move_to(self.left_mass_center()))
        self.right_mass.add_updater(
            lambda m: m.move_to(self.right_mass_center()))

        self.left_mass.get_center = self.left_mass_center
        self.right_mass.get_center = self.right_mass_center

        self.add(self.left_mass, self.right_mass)

    def _create_pulleys(self):
        self.left_pulley = Pulley(self.pulley_radius)
        self.left_pulley.move_to(self.separation / 2 * LEFT)
        self.left_pulley.set_style(**self.pulley_style)

        self.right_pulley = Pulley(self.pulley_radius)
        self.right_pulley.move_to(self.separation / 2 * RIGHT)
        self.right_pulley.set_style(**self.pulley_style)

        self.left_pulley.get_center = self.left_pulley_center
        self.right_pulley.get_center = self.right_pulley_center

        self.left_pulley.add_updater(left_pulley_updater(self))
        self.right_pulley.add_updater(right_pulley_updater(self))

        self.add(self.left_pulley, self.right_pulley)

    def _create_string(self):
        self.string = AtwoodString(self).set_style(**self.string_style)
        self.add(self.string)

    def start(self):
        """Start the simulation."""
        self.add_updater(gravity_updater)

    def stop(self):
        """Stop the simulation."""
        self.remove_updater(gravity_updater)

    def set_velocity(self, v):
        """Set the velocity of the string. This value is used solely to
        predict the motion of the system under the influence of gravity.
        """
        self.v = v

    def set_omega1(self, omega):
        """Set the left pulley angular velocity. This value is used solely
        to predict the motion of the system under the influence of gravity.
        """
        self.omega1 = omega

    def set_omega2(self, omega):
        """Set the right pulley angular velocity. This value is used solely
        to predict the motion of the system under the influence of gravity.
        """
        self.omega2 = omega

    def left_mass_center(self):
        u = polar_to_cartesian(self.pulley_radius, PI -
                               self.theta1.get_value())
        v = polar_to_cartesian(self.l1.get_value(), 3 * PI / 2 -
                               self.theta1.get_value())
        return self.left_pulley_center() + u + v

    def right_mass_center(self):
        u = polar_to_cartesian(self.pulley_radius,
                               self.theta2.get_value())
        v = polar_to_cartesian(self.l2.get_value(),
                               self.theta2.get_value() - PI / 2)
        return self.right_pulley_center() + u + v

    def left_pulley_center(self):
        return self.midpoint_center + LEFT * self.separation / 2

    def right_pulley_center(self):
        return self.midpoint_center + RIGHT * self.separation / 2

    @property
    def midpoint_center(self):
        """The midpoint between the two pulleys"""
        return self.midpoint.get_center()

    def step_solve(self, dt):
        """Solves the differential equation for a dt increment in time."""
        return self.get_graph([0, dt])[1]

    def get_graph(self, t):
        """Solves the differential equation related to the motion of
        the Atwood machine.
        """
        g, r = self.gravity, self.pulley_radius
        m1, m2 = self.m1, self.m2
        l1, l2 = self.l1.get_value(), self.l2.get_value()

        x, v = 0, self.v
        theta1, omega1 = self.theta1.get_value(), self.omega1
        theta2, omega2 = self.theta2.get_value(), self.omega2

        y0 = (x, v, theta1, omega1, theta2, omega2)
        args = (g, r, m1, m2, l1, l2)

        return odeint(atwood_diffeq_system, y0, t, args=args)


def gravity_updater(m: AtwoodMachine, dt):
    """Updater function that describes the motion of the system."""
    x, v, theta1, omega1, theta2, omega2 = m.step_solve(dt)
    l1 = m.l1.get_value() - x + m.pulley_radius * (theta1 - m.theta1.get_value())
    l2 = m.l2.get_value() + x + m.pulley_radius * (theta2 - m.theta2.get_value())

    m.set_velocity(v)
    m.l1.set_value(l1)
    m.l2.set_value(l2)
    m.set_omega1(omega1)
    m.set_omega2(omega2)
    m.theta2.set_value(theta2)
    m.theta1.set_value(theta1)


def left_pulley_updater(atwood: AtwoodMachine):
    """Updater function for the left pulley."""
    old_l = atwood.l1.get_value()
    old_theta = atwood.theta1.get_value()

    def updater(pulley: Mobject):
        nonlocal old_l, old_theta

        dl = atwood.l1.get_value() - old_l
        dtheta = atwood.theta1.get_value() - old_theta
        angle = dl / atwood.pulley_radius - dtheta

        old_l = atwood.l1.get_value()
        old_theta = atwood.theta1.get_value()
        pulley.rotate(angle)
    return updater


def right_pulley_updater(atwood: AtwoodMachine):
    """Updater function for the right pulley."""
    old_l = atwood.l2.get_value()
    old_theta = atwood.theta2.get_value()

    def updater(pulley: Mobject):
        nonlocal old_l, old_theta

        dl = atwood.l2.get_value() - old_l
        dtheta = atwood.theta2.get_value() - old_theta
        angle = dtheta - dl / atwood.pulley_radius

        old_l = atwood.l2.get_value()
        old_theta = atwood.theta2.get_value()
        pulley.rotate(angle)
    return updater
