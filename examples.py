from ita import ITALogo
from atwood import AtwoodMachine
from mechanical_objects import Pulley
from manim import *


class ShowITALogo(Scene):
    def construct(self):
        ita = ITALogo(8)
        self.play(DrawBorderThenFill(ita, run_time=3))
        self.wait()


class ShowAtwood(Scene):
    def construct(self):
        atwood = AtwoodMachine().shift(UP)
        self.add(atwood)
        self.play(atwood.l1.animate.increment_value(1),
                  atwood.theta1.animate.increment_value(30 * DEGREES))
        atwood.start()
        self.wait(10)


class ShowPulley(Scene):
    def construct(self):
        pulley = Pulley(0.4).set_style(
            stroke_color=WHITE,
            stroke_width=0.5 * DEFAULT_STROKE_WIDTH
        )
        self.play(Create(pulley.crosses), Create(pulley.circle))
        self.wait()
