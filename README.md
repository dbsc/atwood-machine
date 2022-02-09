# Atwood Machine Simulation

A simple simulation of an Atwood machine achieved with [manim](https://github.com/ManimCommunity/manim).

<div align="center">
  <img src="simulation.gif" width="600">
</div>

## Mathematical Background

We'll derivate the equations of motion with the aid of [Lagrangian mechanics](https://en.wikipedia.org/wiki/Lagrangian_mechanics)

<div align="center">
  <img src="./tex/atwood_image_white.svg#gh-dark-mode-only" width="450">
  <img src="./tex/atwood_image.svg#gh-light-mode-only" width="450">
</div>

Considering that both pulleys have a radius equal to <img src="./tex/r_white.svg" width="9.3">, we have

<div align="center">
  <img src="./tex/L_equation_white.svg#gh-dark-mode-only" width="490">
  <img src="./tex/L_equation.svg#gh-light-mode-only" width="490">
</div>
<br>
<div align="center">
  <img src="./tex/V_equation_white.svg#gh-dark-mode-only" width="475">
  <img src="./tex/V_equation.svg#gh-light-mode-only" width="475">
</div>
<br>

and the lagrangian will be

<div align="center">
  <img src="./tex/lagrangian_equation_white.svg#gh-dark-mode-only" width="84">
  <img src="./tex/lagrangian_equation.svg#gh-light-mode-only" width="84">
</div>
<br>

Notice the following relation

<div align="center">
  <img src="./tex/relation_equation_white.svg#gh-dark-mode-only" width="174">
  <img src="./tex/relation_equation.svg#gh-light-mode-only" width="174">
</div>
<br>

We can introduce a new variable such that

<div align="center">
  <img src="./tex/x_variable_white.svg#gh-dark-mode-only" width="190.5">
  <img src="./tex/x_variable.svg#gh-light-mode-only" width="190.5">
</div>
<br>

The Lagrangian theory tells us that the system of equations

<div align="center">
  <img src="./tex/lagrangian_system_white.svg#gh-dark-mode-only" width="147.6">
  <img src="./tex/lagrangian_system.svg#gh-light-mode-only" width="147.6">
</div>
<br>

describes the motion of all the particles in the system.

Computing the partial derivatives, we arrive at the following system of differential equations

<div align="center">
  <img src="./tex/final_system_white.svg#gh-dark-mode-only" width="486.6">
  <img src="./tex/final_system.svg#gh-light-mode-only" width="486.6">
</div>
<br>

This system of equations can be solved with the excellent [scipy](https://docs.scipy.org/doc/scipy/reference/) scientific computing library, and in this project, I am using the [odeint](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.odeint.html) function.
