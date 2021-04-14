from manim import *


class ITALogo(VGroup):
    fire_style = {
        "fill_color": RED,
        "fill_opacity": 1,
        "stroke_color": RED,
        "stroke_width": 0 * DEFAULT_STROKE_WIDTH
    }
    letters_style = {
        "fill_color": BLUE,
        "fill_opacity": 1,
        "stroke_color": BLUE,
        "stroke_width": 0 * DEFAULT_STROKE_WIDTH
    }
    triangle_style = {
        "fill_color": WHITE,
        "fill_opacity": 1,
        "stroke_color": WHITE,
        "stroke_width": 0 * DEFAULT_STROKE_WIDTH
    }
    wings_style = {
        "fill_color": YELLOW,
        "fill_opacity": 1,
        "stroke_color": YELLOW,
        "stroke_width": 0 * DEFAULT_STROKE_WIDTH
    }

    def __init__(self, width, **kwargs):
        fire = SVGMobject("svg/ita/fire.svg", False, None).set_style(**self.fire_style)
        letters = SVGMobject("svg/ita/letters.svg", False, None).set_style(**self.letters_style)
        triangle = SVGMobject("svg/ita/triangle.svg", False, None).set_style(**self.triangle_style)
        wings = SVGMobject("svg/ita/wings.svg", False, None).set_style(**self.wings_style)

        mobjects = [fire, letters, triangle, wings]
        super().__init__(*mobjects, **kwargs)
        self.center()
        self.scale_to_fit_width(width)
