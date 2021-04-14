from numpy import sin, cos


def atwood_diffeq_system(y, t, g, r, m1, m2, l1, l2):
    x, v, theta1, omega1, theta2, omega2 = y
    alfa1 = (omega1**2 * r - g * sin(theta1)) / l1
    alfa2 = (omega2**2 * r - g * sin(theta2)) / l2
    a = (m2 * (l2 * omega2**2 + g * cos(theta2)) -
         m1 * (l1 * omega1**2 + g * cos(theta1))) / (m1 + m2)
    return [v, a, omega1, alfa1, omega2, alfa2]
