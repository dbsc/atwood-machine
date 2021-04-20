from misc import stretch
from atwood import AtwoodMachine, AtwoodMachineWithMeasurements
from ita import ITALogo
from manim import *


class IntroScene(Scene):
    def construct(self):
        ita_logo = ITALogo(8)
        ita_text = Tex(r'Instituto Tecnológico \\ de Aeronáutica')
        ita_text.shift(1.5 * DOWN).scale(0.8)
        self.play(DrawBorderThenFill(
            ita_logo,
            run_time=5,
            stroke_width=0.2*DEFAULT_STROKE_WIDTH,
            rate_function=rate_functions.ease_in_expo
        ))
        self.play(
            ita_logo.animate(run_time=0.5).shift(0.5 * UP).scale(0.75),
            Write(ita_text)
        )
        self.play(FadeOut(ita_logo), FadeOut(ita_text))
        self.wait(2)
        sim_text = Tex(r'Simulação de FIS-26 \\[10pt] Máquina de \textit{Atwood}')
        self.play(Write(sim_text))
        self.wait(2)
        self.play(Unwrite(sim_text))


class ShowAtwoodMachine(MovingCameraScene):
    def construct(self):
        atwood = AtwoodMachine()
        atwood.shift(0.8 * UP)
        self.play(Create(atwood.string.left_half),
                  Create(atwood.string.right_half),
                  Create(atwood.left_pulley),
                  Create(atwood.right_pulley), run_time=1)
        self.play(DrawBorderThenFill(atwood.left_mass),
                  DrawBorderThenFill(atwood.right_mass))
        return atwood


class ShowDifferentialEquation(GraphScene, MovingCameraScene):
    def test(self, *args):
        self.add(*args)
        self.wait(1)

    def construct(self):
        ita_logo = ITALogo(8)
        ita_text = Tex(r'Instituto Tecnológico \\ de Aeronáutica')
        ita_text.shift(1.5 * DOWN).scale(0.8)
        self.play(DrawBorderThenFill(
            ita_logo,
            run_time=5,
            stroke_width=0.2*DEFAULT_STROKE_WIDTH,
            rate_function=rate_functions.ease_in_expo
        ))
        self.play(
            ita_logo.animate(run_time=0.5).shift(0.5 * UP).scale(0.75),
            Write(ita_text)
        )
        self.play(FadeOut(ita_logo), FadeOut(ita_text))
        self.wait(2)
        sim_text = Tex(r'Simulação de FIS-26 \\[10pt] Máquina de \textit{Atwood}')
        self.play(Write(sim_text))
        self.wait(2)
        self.play(Unwrite(sim_text))
        self.wait(0.5)
        atwood = AtwoodMachine()
        atwood.shift(0.8 * UP)
        atwood.m2 = 1.022
        self.play(Create(atwood.string.left_half),
                  Create(atwood.string.right_half),
                  Create(atwood.left_pulley),
                  Create(atwood.right_pulley), run_time=1)
        self.play(DrawBorderThenFill(atwood.left_mass),
                  DrawBorderThenFill(atwood.right_mass))
        self.add(atwood)
        left_dashedline = DashedLine(
            atwood.get_left_pulley_center() + DOWN * (atwood.pulley_radius + 0.1),
            atwood.get_left_pulley_center() + DOWN * (atwood.pulley_radius + 0.1 + 1.5),
            dash_length=2 * DEFAULT_DASH_LENGTH,
        ).set_style(stroke_width=0.3 * DEFAULT_STROKE_WIDTH)
        right_dashedline = DashedLine(
            atwood.get_right_pulley_center() + DOWN * (atwood.pulley_radius + 0.1),
            atwood.get_right_pulley_center() + DOWN * (atwood.pulley_radius + 0.1 + 1.5),
            dash_length=2 * DEFAULT_DASH_LENGTH,
        ).set_style(stroke_width=0.3 * DEFAULT_STROKE_WIDTH)
        self.play(atwood.theta1.animate.set_value(30 * DEGREES),
                  atwood.theta2.animate.set_value(30 * DEGREES))
        left_angle = Angle(left_dashedline, atwood.string.left_lower, radius=1,
                           other_angle=True).set_stroke(width=0.5*DEFAULT_STROKE_WIDTH)
        right_angle = Angle(right_dashedline, atwood.string.right_lower, radius=1,
                            other_angle=False).set_stroke(width=0.5*DEFAULT_STROKE_WIDTH)
        theta1 = MathTex(r'\theta_1').scale(0.5).move_to(
            Angle(left_dashedline, atwood.string.left_lower, radius=1 + 3 * SMALL_BUFF, other_angle=True).point_from_proportion(0.5))
        theta2 = MathTex(r'\theta_2').scale(0.5).move_to(
            Angle(right_dashedline, atwood.string.right_lower, radius=1 + 3 * SMALL_BUFF, other_angle=False).point_from_proportion(0.5))
        m1 = MathTex(r'm_1').scale(0.5).add_updater(lambda m: m.move_to(
            atwood.get_left_mass_position() + DOWN * MED_SMALL_BUFF * 1.5))
        m2 = MathTex(r'm_2').scale(0.5).add_updater(lambda m: m.move_to(
            atwood.get_right_mass_position() + DOWN * MED_SMALL_BUFF * 1.5))

        def stretch(m, get_angle, value):
            m.rotate(get_angle())
            m.stretch_to_fit_width(value)
            m.rotate(-get_angle())
            return m
        left_brace = Brace(atwood.string.left_lower, direction=atwood.string.left_lower.copy(
        ).rotate(-PI/2).get_unit_vector(), buff=2*SMALL_BUFF)
        right_brace = Brace(atwood.string.right_lower, direction=atwood.string.right_lower.copy(
        ).rotate(PI/2).get_unit_vector(), buff=2*SMALL_BUFF)
        left_brace.rotate(atwood.theta1.get_value())
        left_brace.stretch_to_fit_width(0.14)
        left_brace.rotate(-atwood.theta1.get_value())
        right_brace.rotate(-atwood.theta2.get_value())
        right_brace.stretch_to_fit_width(0.14)
        right_brace.rotate(atwood.theta2.get_value())
        Line().get_unit_vector()
        l1 = left_brace.get_tex('l_1').scale(0.5).add_updater(lambda m: m.move_to(left_brace.get_center(
        ) + atwood.string.left_lower.copy().rotate(-PI/2).get_unit_vector() * MED_SMALL_BUFF * 1.5))
        # self.add(Line(ORIGIN, atwood.string.left_lower.copy().rotate(-PI/2).get_unit_vector()))
        l2 = right_brace.get_tex('l_2').scale(0.5).add_updater(lambda m: m.move_to(right_brace.get_center(
        ) + atwood.string.right_lower.copy().rotate(PI/2).get_unit_vector() * MED_SMALL_BUFF * 1.5))
        l2.get_
        self.play(Create(left_dashedline), Create(right_dashedline),
                  FadeInFrom(left_brace, atwood.string.left_lower.copy(
                  ).rotate(-PI/2).get_unit_vector()),
                  FadeInFrom(right_brace, atwood.string.right_lower.copy().rotate(PI/2).get_unit_vector()))
        self.play(Create(theta1), Create(theta2), Create(left_angle), Create(
            right_angle), Create(l1), Create(l2), Create(m1), Create(m2))
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.shift(1.5 * DOWN))
        theta1_eq = MathTex(
            r'l_1\ddot{\theta_1} + 2\dot{l_1}\dot{\theta_1} = -g\sin\theta_1 + r\dot{\theta_1}^2')
        theta2_eq = MathTex(
            r'l_2\ddot{\theta_2} + 2\dot{l_2}\dot{\theta_2} = -g\sin\theta_2 + r\dot{\theta_2}^2')
        x_equation = MathTex(
            r'(m_1 + m_2)\ddot{x} = -m_1g\cos\theta_1 + m_2g\cos\theta_2 - m_1l_1\dot{\theta_1}^2 + m_2l_2\dot{\theta_2}^2')
        v_equation = MathTex(
            r'\dot{x} = \dot{l_2} - r\dot{\theta_2} = -\dot{l_1} + r\dot{\theta_1}')
        equations = VGroup(x_equation, theta1_eq, theta2_eq, v_equation).arrange(
            DOWN * MED_LARGE_BUFF * 2).scale(0.7)
        equations.shift(DOWN * 3)
        self.play(Write(theta1_eq), Write(theta2_eq),
                  Write(x_equation), Write(v_equation))
        self.wait(5)
        self.play(Unwrite(theta1_eq), Unwrite(theta2_eq),
                  Unwrite(x_equation), Unwrite(v_equation))
        # self.play(self.camera.frame.animate.shift(1.5 * DOWN))
        # self.add(l1, l2, left_brace, right_brace, theta1, theta2, left_angle, right_angle, left_dashedline, right_dashedline)
        self.play(Uncreate(right_angle), Uncreate(
            right_dashedline), Uncreate(theta2))
        left_brace.add_updater(lambda m: m.become(stretch(
            Brace(atwood.string.left_lower, direction=atwood.string.left_lower.copy(
            ).rotate(-PI/2).get_unit_vector(), buff=2*SMALL_BUFF, min_num_quads=4),
            atwood.theta1.get_value,
            0.14
        )))
        right_brace.add_updater(lambda m: m.become(stretch(
            Brace(atwood.string.right_lower, direction=atwood.string.right_lower.copy(
            ).rotate(PI/2).get_unit_vector(), buff=2*SMALL_BUFF, min_num_quads=4),
            lambda: -atwood.theta2.get_value(),
            0.14
        )))
        l1_value = MathTex(r'1\,\mathrm{m}').scale(0.5).add_updater(lambda m: m.move_to(left_brace.get_center(
        ) + atwood.string.left_lower.copy().rotate(-PI/2).get_unit_vector() * MED_SMALL_BUFF * 1.5))
        l2_value = MathTex(r'4\,\mathrm{m}').scale(0.5).add_updater(
            lambda m: m.move_to(right_brace.get_center() + RIGHT * 1.5 * MED_SMALL_BUFF))
        m1_value = MathTex(r'1.022\,\mathrm{kg}').scale(0.5).add_updater(
            lambda m: m.move_to(atwood.get_left_mass_position() + DOWN * MED_SMALL_BUFF * 1.5))
        m2_value = MathTex(r'1\,\mathrm{kg}').scale(0.5).add_updater(lambda m: m.move_to(
            atwood.get_right_mass_position() + DOWN * MED_SMALL_BUFF * 1.5))
        left_angle_new = Angle(left_dashedline, atwood.string.left_lower, radius=0.8,
                               other_angle=True).set_stroke(width=0.5*DEFAULT_STROKE_WIDTH)
        theta1_value = MathTex(r'30^{\circ}').scale(0.4).move_to(Angle(
            left_dashedline, atwood.string.left_lower, radius=1, other_angle=True).point_from_proportion(0.5))
        self.play(atwood.theta2.animate.set_value(0), atwood.l1.animate.increment_value(-1), atwood.l2.animate.increment_value(3),
                  Transform(l2, l2_value), Transform(l1, l1_value), Transform(
                      m1, m1_value), Transform(theta1, theta1_value),
                  Transform(left_angle, left_angle_new), Transform(
                      m2, m2_value)
                  )
        self.wait(3)
        self.play(Uncreate(l1), Uncreate(l2), Uncreate(m1), Uncreate(m2), Uncreate(theta1), Uncreate(
            left_angle), Uncreate(left_brace), Uncreate(right_brace), Uncreate(left_dashedline))
        self.wait(1)

        trace = TracedPath(atwood.get_left_mass_position, min_distance_to_new_point=0.001,
                           stroke_width=0.75 * DEFAULT_STROKE_WIDTH, stroke_color=PINK, stroke_opacity=0.5)
        self.add(trace)
        self.bring_to_back(trace)
        atwood.set_speed(1)
        self.wait(40)
        atwood.set_speed(2.5)
        self.wait(40)
        atwood.set_speed(5)
        self.wait(40)
        atwood.set_speed(0)
        self.wait(1)
        self.play(Uncreate(atwood.string.left_half),
                  Uncreate(atwood.string.right_half),
                  Uncreate(atwood.left_pulley),
                  Uncreate(atwood.right_pulley), Uncreate(
                      atwood.left_mass), Uncreate(atwood.right_mass), Uncreate(trace),
                  run_time=1.5)
        self.wait(1)


class TestScene(MovingCameraScene):
    def construct(self):
        atwood = AtwoodMachine()
        atwood.shift(0.8 * UP)
        atwood.theta1.set_value(40 * DEGREES)
        self.play(Create(atwood.string.left_half),
                  Create(atwood.string.right_half),
                  Create(atwood.left_pulley),
                  Create(atwood.right_pulley), run_time=1)
        self.play(DrawBorderThenFill(atwood.left_mass),
                  DrawBorderThenFill(atwood.right_mass))
        # self.add(atwood)
        atwood.m2 = 1.021
        trace = TracedPath(atwood.get_left_mass_position, min_distance_to_new_point=0.001,
                           stroke_width=0.75 * DEFAULT_STROKE_WIDTH, stroke_color=PINK, stroke_opacity=0.5)
        self.add(trace)
        self.bring_to_back(trace)
        atwood.start()
        self.wait(5)


class PlayAtwoodMachine(GraphScene, MovingCameraScene):
    def construct(self):
        atwood = AtwoodMachine()
        self.add(atwood)
        atwood.shift(2.5 * UP)
        atwood.m2 = 1.022
        atwood.l1.increment_value(-1)
        atwood.l2.increment_value(3)
        atwood.theta1.set_value(30 * DEGREES)
        trace = TracedPath(atwood.get_left_mass_position, min_distance_to_new_point=0.001,
                           stroke_width=DEFAULT_STROKE_WIDTH, stroke_color=PINK, stroke_opacity=0.5)
        self.add(trace)
        self.bring_to_back(trace)
        atwood.start()
        atwood.set_speed(2)
        self.wait(5)
        # self.play(Uncreate(atwood.string.left_half),
        #           Uncreate(atwood.string.right_half),
        #           Uncreate(atwood.left_pulley),
        #           Uncreate(atwood.right_pulley), Uncreate(atwood.left_mass), Uncreate(atwood.right_mass), run_time=1)
        # TracedPath
        # MoveAlongPath


class AtwoodScene(MovingCameraScene):
    def construct(self):
        IntroScene.construct(self)
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
        self.play(atwood.theta1.animate.set_value(30 * DEGREES), atwood.theta2.animate.set_value(
            5 * DEGREES), atwood.l2.animate.set_value(4), atwood.animate.shift(UP))

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


class AllScenes(Scene):
    def construct(self):
        import numpy as np
        import matplotlib.pyplot as plt
        at = AtwoodMachine()
        at.theta1.set_value(3.14 / 6)
        t = np.linspace(0, 10, 500)
        sol = at.get_graph(t)
        func = lambda t: (sol[int(t * 50) + 1][2] - sol[int(t * 50)][2]) * rate_functions.linear(t * 50 - int(t * 50)) + sol[int(t * 50)][2]
        self.add(FunctionGraph(func, x_min=0, x_max=5))
        self.wait(1)
