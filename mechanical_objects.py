from itertools import chain
from manim import *
from polar import cartesian_to_polar, polar_to_cartesian
# from atwood import AtwoodMachine


class PhantomPoint(Square):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_style(fill_opacity=0, stroke_opacity=0)
        self.original_height = self.height

    @property
    def current_scale(self):
        return self.height / self.original_height


class Mass(Circle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Pulley(VGroup):

    def __init__(self, radius, num, ratio, **kwargs):
        circle = Circle(radius=radius)
        crosses = []
        for i in range(num):
            crosses.append(Line(0.5 * ratio * LEFT, 0.5 * ratio *
                           RIGHT).rotate(PI * i / num))
        super().__init__(circle, *crosses, **kwargs)


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
        return self.atwood.current_pulley_radius

    @property
    def string_center(self):
        return self.atwood.fixed_center.get_center() + UP * self.radius

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
        return self.atwood.left_mass.radius * self.atwood.current_scale

    @property
    def right_mass_radius(self):
        return self.atwood.right_mass.radius * self.atwood.current_scale

class AtwoodStringV0(VGroup):

    def __init__(self, atwood, **kwargs):
        self.atwood = atwood

        def get_left_half(radius, fixed_point, pulley, mass, theta):
            middle = Line(fixed_point.get_center() + radius * UP,
                          pulley.get_center() + radius * UP).get_points()
            arc = Arc(PI / 2, PI / 2 - theta.get_value(), radius=radius,
                      arc_center=pulley.get_center()).get_points()
            lower = Line(pulley.get_center() + polar_to_cartesian(radius, PI - theta.get_value()),
                         mass.get_center() + polar_to_cartesian(mass.radius, PI / 2 - theta.get_value())).get_points()
            return [p for p in chain(middle, arc, lower)]

        def get_right_half(radius, fixed_point, pulley, mass, theta):
            middle = Line(fixed_point.get_center() + radius * UP,
                          pulley.get_center() + radius * UP).get_points()
            arc = Arc(PI / 2, theta.get_value() - PI / 2, radius=radius,
                      arc_center=pulley.get_center()).get_points()
            lower = Line(pulley.get_center() + polar_to_cartesian(radius, theta.get_value()),
                         mass.get_center() + polar_to_cartesian(mass.radius, PI / 2 + theta.get_value())).get_points()
            return [p for p in chain(middle, arc, lower)]
        pulley_radius = self.radius
        fixed_point = self.atwood.fixed_center
        left_pulley = self.atwood.left_pulley
        right_pulley = self.atwood.right_pulley
        left_mass = self.atwood.left_mass
        right_mass = self.atwood.right_mass
        theta1 = self.atwood.theta1
        theta2 = self.atwood.theta2
        self.left_half = Line().add_updater(lambda m: m.set_points(
            get_left_half(pulley_radius, fixed_point, left_pulley, left_mass, theta1)))
        self.right_half = Line().add_updater(lambda m: m.set_points(
            get_right_half(pulley_radius, fixed_point, right_pulley, right_mass, theta2)))
        super().__init__(self.left_half, self.right_half, **kwargs)

    @property
    def radius(self):
        return self.atwood.pulley_radius