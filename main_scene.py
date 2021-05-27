from ita import ITALogo
from atwood import AtwoodMachine, TreatMachine
from mechanical_objects import Pulley
from manim import *


class MainScene(MovingCameraScene):
    def construct(self):
        atwood = AtwoodMachine()
        atwood.shift(1.5 * UP)
        atwood.m2 = 1.008

        self.play(Create(atwood.string.left_half),
                  Create(atwood.string.right_half),
                  Create(atwood.left_pulley),
                  Create(atwood.right_pulley), run_time=1)
        self.play(DrawBorderThenFill(atwood.left_mass),
                  DrawBorderThenFill(atwood.right_mass))
        self.add(atwood)
        self.wait(0.1)
        axes = Axes(
            x_range=[-PI/6, PI/6, PI/24],
            y_range=[0, 4.5, 0.5],
            x_length=4,
            y_length=4,
            axis_config={"include_tip": False},
        )
        axes.shift(4.5 * UP)
        l = MathTex('l').scale(0.75).move_to(axes).shift(UP * 2.4)
        theta = MathTex('\\theta').scale(0.75).move_to(axes).shift(DOWN * 2, RIGHT * 2.3)

        self.play(atwood.theta1.animate.set_value(15 * DEGREES),
                  atwood.l1.animate.set_value(1),
                  atwood.l2.animate.increment_value(1.5))
        self.play(self.camera.frame.animate.shift(2.75 * UP).scale(1.5),
                  Write(axes))

        def dot1_updater(m):
            l1 = atwood.l1.get_value()
            theta1 = atwood.theta1.get_value()
            m.move_to(axes.coords_to_point(theta1, l1))

        def dot2_updater(m):
            l2 = atwood.l2.get_value()
            theta2 = atwood.theta2.get_value()
            m.move_to(axes.coords_to_point(theta2, l2))

        dot1 = Dot(color=BLUE).add_updater(dot1_updater)
        dot2 = Dot(color=RED).add_updater(dot2_updater)

        self.play(Create(dot1), Create(dot2), Write(l), Write(theta))

        trace1 = TracedPath(
            dot1.get_center,
            min_distance_to_new_point=0.001,
            stroke_width=0.4*DEFAULT_STROKE_WIDTH,
            stroke_color=BLUE
        )
        trace2 = TracedPath(
            dot2.get_center,
            min_distance_to_new_point=0.001,
            stroke_width=0.4*DEFAULT_STROKE_WIDTH,
            stroke_color=RED
        )
        self.add(trace1, trace2)
        atwood.start()
        self.wait(60)
