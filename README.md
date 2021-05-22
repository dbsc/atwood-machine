
# Atwood Machine Simulation

A simple simulation of an Atwood machine achieved with [manim](github.com).

If you can't see the figures and/or the equations, please checkout the [light theme version of this README](README_light.md).

## Mathematical Background

We'll derivate the equations of motion with the aid of [Lagrangian mechanics](https://en.wikipedia.org/wiki/Lagrangian_mechanics)

<!-- Dimesions of each image -->

<!-- atwood_image 1082
final_system 1170
lagrangian_equation 202
lagrangian_system 355
L_equation 1178
r 20
relation_equation 418
V_equation 1113
x_variable 458 -->

<div align="center">
  <img src="./tex/atwood_image_white.svg" width="450">
</div>

Considering the pulley to have a radius   <img src="./tex/r_white.svg" width="9.3">, we have

<div align="center">
  <img src="./tex/L_equation_white.svg" width="550">
</div>
<br>
<div align="center">
  <img src="./tex/V_equation_white.svg" width="519">
</div>
<br>

and the lagrangian will be

<div align="center">
  <img src="./tex/lagrangian_equation_white.svg" width="94.3">
</div>

Notice the following relation

<div align="center">
  <img src="./tex/relation_equation_white.svg" width="195">
</div>

We can introduce a new variable such that

<div align="center">
  <img src="./tex/x_variable_white.svg" width="214">
</div>

The Lagrangian theory will tell us that we have the following system describes the motion of system

<div align="center">
  <img src="./tex/lagrangian_system_white.svg" width="165.7">
</div>

Computing the partial derivatives, we arrive at the following system of differential equations

<div align="center">
  <img src="./tex/final_system_white.svg" width="546">
</div>

This system of equations can be solved with the excellent [scipy](https://docs.scipy.org/doc/scipy/reference/) scientific computing library, and in this case, we are using the [odeint](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.odeint.html) function.
