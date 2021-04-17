from polar import polar_to_cartesian
from itertools import chain
from manim import *


class Mass(Circle):
    Circle
    def __init__(self, radius, *args, **kwargs):
        super().__init__(*args, radius=radius, **kwargs)


class Pulley(VGroup):

    def __init__(self, radius, num, ratio, **kwargs):
        self.circle = Circle(radius=radius)
        crosses = []
        for i in range(num):
            crosses.append(Line(0.5 * ratio * LEFT, 0.5 * ratio *
                           RIGHT).rotate(PI * i / num))
        self.crosses = VGroup(*crosses)
        super().__init__(self.circle, self.crosses, **kwargs)


class AtwoodString(VGroup):

    def __init__(self, atwood, **kwargs):
        self.atwood = atwood
        self.left_half = Line().add_updater(lambda m: m.set_points(self.get_left_half()))
        self.right_half = Line().add_updater(lambda m: m.set_points(self.get_right_half()))
        super().__init__(self.left_half, self.right_half, **kwargs)

    def get_left_half(self):
        middle = Line(self.string_center, self.left_pulley_center +
                      UP * self.radius).get_points()
        arc = Arc(PI / 2, PI / 2 - self.theta1, self.radius,
                  arc_center=self.left_pulley_center).get_points()
        lower = Line(self.left_pulley_center + polar_to_cartesian(self.radius, PI - self.theta1),
                     self.left_mass_center + polar_to_cartesian(self.left_mass_radius, PI / 2 - self.theta1)).get_points()
        return [p for p in chain(middle, arc, lower)]

    def get_right_half(self):
        middle = Line(self.string_center,
                      self.right_pulley_center + UP * self.radius).get_points()
        arc = Arc(PI / 2, self.theta2 - PI / 2, self.radius,
                  arc_center=self.right_pulley_center).get_points()
        lower = Line(self.right_pulley_center + polar_to_cartesian(self.radius, self.theta2),
                     self.right_mass_center + polar_to_cartesian(self.right_mass_radius, PI / 2 + self.theta2)).get_points()
        return [p for p in chain(middle, arc, lower)]

    @property
    def radius(self):
        return self.atwood.pulley_radius

    @property
    def string_center(self):
        return self.atwood.fixed_center + UP * self.radius

    @property
    def left_pulley_center(self):
        return self.atwood.left_pulley.get_center()

    @property
    def right_pulley_center(self):
        return self.atwood.right_pulley.get_center()

    @property
    def left_mass_center(self):
        return self.atwood.get_left_mass_position()

    @property
    def right_mass_center(self):
        return self.atwood.get_right_mass_position()

    @property
    def theta1(self):
        return self.atwood.theta1.get_value()

    @property
    def theta2(self):
        return self.atwood.theta2.get_value()

    @property
    def l1(self):
        return self.atwood.l1.get_value()

    @property
    def l2(self):
        return self.atwood.l2.get_value()

    @property
    def left_mass_radius(self):
        return self.atwood.left_mass.radius

    @property
    def right_mass_radius(self):
        return self.atwood.right_mass.radius
