from numpy import sin, cos, arccos, sqrt
from numpy.linalg import norm
from manim import RIGHT, UP, PI


def polar_to_cartesian(r, theta):
    return r * (RIGHT * cos(theta) + UP * sin(theta))


def cartesian_to_polar(vector):
    x, y, _ = vector
    r = sqrt(x**2 + y**2)
    if y >= 0:
        theta = arccos(x / r)
    else:
        theta = 2 * PI - arccos(x / r)
    return (r, theta)


def stretch(mobject, factor, direction):
    theta = cartesian_to_polar(direction)[1]
    mobject.rotate(-theta)
    mobject.stretch(factor, 0)
    mobject.rotate(theta)
    return mobject