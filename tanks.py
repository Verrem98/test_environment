import matplotlib.pyplot as plt
import numpy as np


def plot_solution(results):
    x, y = results

    plt.plot(x, 'r', label='tank1')
    plt.plot(y, 'b', label='tank2')
    plt.xlabel('minuten')
    plt.ylabel('zoutoplossing (kg)')
    plt.legend()
    plt.show()


def f(yt1, yt2):
    st1 = 1.2 + (1 / 100 * yt2) - (3 / 100 * yt1) - (4 / 100 * yt1)
    st2 = (3 / 100 * yt1) - (2 / 100 * yt2) - (1 / 100 * yt2)

    return st1, st2


def solve_with_forward_euler(f, h, x_min, x_max):
    """
    solves a set of two ODEs using forward euler

    :param f: The function that we use to calculate the derivative
    :param h: Stepsize
    :param x_min: Minimum x-axis value
    :param x_max: Maximum x-axis value (not inclusive)
    :return: a list of floats for tank1, a list of floats for tank2
    """

    t = np.arange(x_min, x_max, h)

    t1 = np.zeros(len(t))
    t2 = np.zeros(len(t))

    # tank 2 starts with a salt weight of 20
    t2[0] = 20

    # use forward euler to calculate the new values
    for i in range(len(t) - 1):
        t1[i + 1] = t1[i] + f(t1[i], t2[i])[0] * h
        t2[i + 1] = t2[i] + f(t1[i], t2[i])[1] * h

    return t1, t2


def solve_with_heun(f, h, x_min, x_max):
    """

    solves a set of two ODEs using heun's method

    :param f: The function that we use to calculate the derivative
    :param h: Stepsize
    :param x_min: Minimum x-axis value
    :param x_max: Maximum x-axis value (not inclusive)
    :return: a list of floats for tank1, a list of floats for tank2
    """

    t = np.arange(x_min, x_max, h)

    t1 = np.zeros(len(t))
    t2 = np.zeros(len(t))

    # tank 2 starts with a salt weight of 20
    t2[0] = 20

    # use heun's method to calculate the new values
    for i in range(len(t) - 1):
        sl = h * f(t1[i], t2[i])[0]
        sr = h * f(t1[i] + sl, t2[i])[0]
        t1[i + 1] = t1[i] + (sl + sr) / 2

        sl = h * f(t1[i], t2[i])[1]
        sr = h * f(t1[i] + sl, t2[i])[1]
        t2[i + 1] = t2[i] + (sl + sr) / 2

    return t1, t2


plot_solution(solve_with_forward_euler(f, 0.01, 0, 200))
plot_solution(solve_with_heun(f, 0.01, 0, 200))
