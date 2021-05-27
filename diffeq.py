from typing import List
from numpy import sin, cos


def atwood_diffeq_system(
    y: List[float],
    t: float,
    g: float = 9.86,
    r: float = 0.1,
    m1: float = 1,
    m2: float = 1,
    l1: float = 1,
    l2: float = 1,
) -> List[float]:
    """The set of equations that describe the motion of the system.

    :param y: A list of variables, which are:
              - `x`: a value measures the position of the string
              - `v`: the derivative of x with respect to time
              - `theta1`: the angle between the left string and the vertical
              - `omega1`: the derivate of `theta1` with respect to time
              - `theta2`: the angle between the right string and the vertical
              - `omega2`: theta derivative of `theta2` with respect to time
    :param t: The time in seconds. This value does not really matter, but must
              be listed here for the sake of the differential equation solving
              algorithm employed by numpy.
    :param g: The value of gravity in meters per second squared.
    :param r: The radius of the pulleys in meters.
    :param m1: The mass of the left mass in kilograms.
    :param m2: The mass of the right mass in kilograms.
    :param l1: The length of the left side string, from where it touches the
               pulley to the center of the left mass.
    :param l2: The length of the right side string, from where it touches the
               pulley to the center of the right mass.
    :returns: The derivative of `y` with respect to time. This function does
              not calculate the derivative of `y` in a general case; just when
              the motion of the system matches that of an Atwood Machine
    """
    x, v, theta1, omega1, theta2, omega2 = y
    alfa1 = (omega1**2 * r - g * sin(theta1) -
             2 * (r * omega1 - v) * omega1) / l1
    alfa2 = (omega2**2 * r - g * sin(theta2) -
             2 * (v + r * omega2) * omega2) / l2
    a = (m2 * (l2 * omega2**2 + g * cos(theta2)) -
         m1 * (l1 * omega1**2 + g * cos(theta1))) / (m1 + m2)
    return [v, a, omega1, alfa1, omega2, alfa2]
