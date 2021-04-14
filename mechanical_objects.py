from itertools import chain
from manim import *
from polar import cartesian_to_polar, polar_to_cartesian


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

    def __init__(self, pulley_radius, fixed_point, left_pulley, right_pulley, left_mass, right_mass, theta1, theta2, **kwargs):
        def get_left_half(radius, fixed_point, pulley, mass, theta):
            middle = Line(fixed_point.get_center() + radius * UP, pulley.get_center() + radius * UP).get_points()
            arc = Arc(PI / 2, PI / 2 - theta.get_value(), radius=radius, arc_center=pulley.get_center()).get_points()
            lower = Line(pulley.get_center() + polar_to_cartesian(radius, PI - theta.get_value()),
                           mass.get_center() + polar_to_cartesian(mass.radius, PI / 2 - theta.get_value())).get_points()
            return [p for p in chain(middle, arc, lower)]
        def get_right_half(radius, fixed_point, pulley, mass, theta):
            middle = Line(fixed_point.get_center() + radius * UP, pulley.get_center() + radius * UP).get_points()
            arc = Arc(PI / 2, theta.get_value() - PI / 2, radius=radius, arc_center=pulley.get_center()).get_points()
            lower = Line(pulley.get_center() + polar_to_cartesian(radius, theta.get_value()),
                           mass.get_center() + polar_to_cartesian(mass.radius, PI / 2 + theta.get_value())).get_points()
            return [p for p in chain(middle, arc, lower)]
        self.left_half = Line().add_updater(lambda m: m.set_points(get_left_half(pulley_radius, fixed_point, left_pulley, left_mass, theta1)))
        self.right_half = Line().add_updater(lambda m: m.set_points(get_right_half(pulley_radius, fixed_point, right_pulley, right_mass, theta2)))
        super().__init__(self.left_half, self.right_half)
