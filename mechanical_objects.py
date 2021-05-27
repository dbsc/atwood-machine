from misc import polar_to_cartesian
from itertools import chain
from manim import *
from colour import Color


class Mass(Circle):

    def __init__(self, radius, *args, **kwargs):
        super().__init__(*args, radius=radius, **kwargs)


class TreatPulley(VGroup):
    white_style = {
        "fill_color": Color('#dfe5e8'),
        "fill_opacity": 1,
        "stroke_color": BLACK,
        "stroke_width": 0 * DEFAULT_STROKE_WIDTH,
        "stroke_opacity": 0,
    }
    red_style = {
        "fill_color": Color("#f4536a"),
        "fill_opacity": 1,
        "stroke_color": BLACK,
        "stroke_width": 0 * DEFAULT_STROKE_WIDTH,
        "stroke_opacity": 0,
    }

    def __init__(self, radius, **kwargs):
        red = SVGMobject("svg/pulley_white.svg", False,
                         None).set_style(**self.red_style)
        white = SVGMobject("svg/pulley_red.svg", False,
                           None).set_style(**self.white_style)

        mobjects = [white, red]
        super().__init__(*mobjects, **kwargs)
        self.center()
        self.scale_to_fit_width(2 * radius)


class Pulley(VGroup):

    def __init__(self, radius, num=3, ratio=0.5, **kwargs):
        self.circle = Circle(radius=radius)
        line = Line(ratio * LEFT, ratio * RIGHT)
        crosses = []
        for i in range(num):
            crosses.append(line.copy().rotate(PI * i / num))
        self.crosses = VGroup(*crosses)
        super().__init__(self.circle, self.crosses, **kwargs)


class AtwoodString(VGroup):

    def __init__(self, atwood, **kwargs):
        self.atwood = atwood
        self.left_half = f_always(Line().set_points, self.get_left_half)
        self.right_half = f_always(Line().set_points, self.get_right_half)
        super().__init__(self.left_half, self.right_half, **kwargs)

    def get_left_half(self):
        self.left_middle = Line(
            self.string_center,
            self.left_pulley_center + UP * self.radius
        )
        self.left_arc = Arc(
            start_angle=PI / 2,
            angle=PI / 2 - self.theta1,
            radius=self.radius,
            arc_center=self.left_pulley_center
        )
        self.left_lower = Line(
            self.left_pulley_center +
            polar_to_cartesian(self.radius, PI - self.theta1),
            self.left_mass_center +
            polar_to_cartesian(self.left_mass_radius, PI / 2 - self.theta1)
        )
        parts = [self.left_middle, self.left_arc, self.left_lower]
        return [p for p in chain(*[m.get_points() for m in parts])]

    def get_right_half(self):
        self.right_middle = Line(
            self.string_center,
            self.right_pulley_center + UP * self.radius
        )
        self.right_arc = Arc(
            start_angle=PI / 2,
            angle=self.theta2 - PI / 2,
            radius=self.radius,
            arc_center=self.right_pulley_center
        )
        self.right_lower = Line(
            self.right_pulley_center +
            polar_to_cartesian(self.radius, self.theta2),
            self.right_mass_center +
            polar_to_cartesian(self.right_mass_radius, PI / 2 + self.theta2)
        )
        parts = [self.right_middle, self.right_arc, self.right_lower]
        return [p for p in chain(*[m.get_points() for m in parts])]

    @property
    def left_line(self):
        self.get_left_half()
        return self.left_lower

    @property
    def right_line(self):
        self.get_right_half()
        return self.left_lower

    @property
    def radius(self):
        return self.atwood.pulley_radius

    @property
    def string_center(self):
        return self.atwood.midpoint_center + UP * self.radius

    @property
    def left_pulley_center(self):
        return self.atwood.left_pulley_center()

    @property
    def right_pulley_center(self):
        return self.atwood.right_pulley_center()

    @property
    def left_mass_center(self):
        return self.atwood.left_mass_center()

    @property
    def right_mass_center(self):
        return self.atwood.right_mass_center()

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
