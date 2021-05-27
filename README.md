
# Atwood Machine Simulation

A simple simulation of an Atwood machine achieved with [manim](github.com).

If you can't see the figures and/or the equations, please checkout the [light theme version of this README](README_light.md).

<div align="center">
  <img src="simulation.gif" width="600">
</div>

<div align="center">
  <img src="ita_logo.gif" width="600">
</div>

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

Considering that both pulleys have a radius equal to <img src="./tex/r_white.svg" width="9.3">, we have

<div align="center">
  <img src="./tex/L_equation_white.svg" width="490">
</div>
<br>
<div align="center">
  <img src="./tex/V_equation_white.svg" width="475">
</div>
<br>

and the lagrangian will be

<div align="center">
  <img src="./tex/lagrangian_equation_white.svg" width="84">
</div>
<br>

Notice the following relation

<div align="center">
  <img src="./tex/relation_equation_white.svg" width="174">
</div>
<br>

We can introduce a new variable such that

<div align="center">
  <img src="./tex/x_variable_white.svg" width="190.5">
</div>
<br>

The Lagrangian theory tells us that the system of equations

<div align="center">
  <img src="./tex/lagrangian_system_white.svg" width="147.6">
</div>
<br>

describes the motion of all the particles in the system.

Computing the partial derivatives, we arrive at the following system of differential equations

<div align="center">
  <img src="./tex/final_system_white.svg" width="486.6">
</div>
<br>

This system of equations can be solved with the excellent [scipy](https://docs.scipy.org/doc/scipy/reference/) scientific computing library, and in this project, I am using the [odeint](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.odeint.html) function.
