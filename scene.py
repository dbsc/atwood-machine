from manim.utils.rate_functions import ease_in_out_elastic, ease_out_back, ease_out_bounce
from atwood import AtwoodMachine
from ita import ITALogo
from manim import *


class ITAScene(MovingCameraScene):
    def construct(self):
        text = Tex(r'Instituto Tecnológico \\ de Aeronáutica').shift(2 * DOWN)
        ita = ITALogo(10)
        self.play(DrawBorderThenFill(ita, run_time=5, stroke_width=0.2*DEFAULT_STROKE_WIDTH, rate_function=rate_functions.ease_in_expo))
        self.play(ita.animate(run_time=0.5).shift(0.5 * UP).scale(0.65), Write(text))
        self.wait(1)
        self.play(FadeOut(ita), FadeOut(text))
        text2 = Tex(r'Simulação de FIS-32 \\[10pt] Máquina de Atwood')
        self.play(Write(text2))
        self.wait(1)
        self.play(Unwrite(text2))


class AtwoodScene(MovingCameraScene):
    def construct(self):
        ITAScene.construct(self)
        atwood = AtwoodMachine()
        atwood.center()
        self.camera.frame.save_state()
        self.camera.frame.scale(0.5)
        atwood.shift(0.4 * UP)
        self.show_atwood(atwood)
        self.show_movement(atwood)
        # self.camera.frame.scale(1.5)
        # self.add(atwood)
        self.play(self.camera.frame.animate.scale(1.5))
        self.play(atwood.theta1.animate.set_value(30 * DEGREES), atwood.theta2.animate.set_value(5 * DEGREES), atwood.l2.animate.set_value(4), atwood.animate.shift(UP))

        atwood.start_animation()


        self.wait(18)

    def show_atwood(self, atwood):
        self.play(Create(atwood.left_pulley),
                  Create(atwood.right_pulley),
                  Create(atwood.string.left_half),
                  Create(atwood.string.right_half))
        self.play(DrawBorderThenFill(atwood.left_mass, stroke_width=0.25*DEFAULT_STROKE_WIDTH, stroke_color=WHITE),
                  DrawBorderThenFill(atwood.right_mass, stroke_width=0.25*DEFAULT_STROKE_WIDTH, stroke_color=WHITE), run_time=1.5)

    def show_movement(self, atwood):
        self.play(atwood.theta1.animate.set_value(35 * DEGREES),
                  atwood.theta2.animate.set_value(35 * DEGREES))
        self.play(atwood.theta1.animate(run_time=2).set_value(-25 * DEGREES),
                  atwood.theta2.animate(run_time=2).set_value(-25 * DEGREES))
        self.play(atwood.theta1.animate.set_value(0),
                  atwood.theta2.animate.set_value(0))
        self.play(self.camera.frame.animate.scale(1.5))
        self.play(atwood.l1.animate.increment_value(1),
                  atwood.l2.animate.increment_value(-1))
        self.play(atwood.l1.animate(run_time=2).increment_value(-2),
                  atwood.l2.animate(run_time=2).increment_value(2))
        self.play(atwood.l1.animate.increment_value(1),
                  atwood.l2.animate.increment_value(-1))
