from manim import *

class ITALogo(VGroup):

    def __init__(self, width, **kwargs):
        fire = SVGMobject("ita/fire.svg", False, None).set_style(
            fill_color=WHITE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=DEFAULT_STROKE_WIDTH
        )
        letters = SVGMobject("ita/letters.svg", False, None).set_style(
            fill_color=WHITE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=DEFAULT_STROKE_WIDTH
        )
        triangle = SVGMobject("ita/triangle.svg", False, None).set_style(
            fill_color=WHITE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=DEFAULT_STROKE_WIDTH
        )
        wings = SVGMobject("ita/wings.svg", False, None).set_style(
            fill_color=WHITE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=DEFAULT_STROKE_WIDTH
        )
        mobjects = [fire, letters, triangle, wings]
        super().__init__(*mobjects, **kwargs)
        self.center()
        self.scale_to_fit_width(width)
