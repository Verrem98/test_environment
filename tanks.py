from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np


def generate_graph(lower_lim, upper_lim, step_size):

    def model(y, t):
        yt1, yt2 = y

        st1 = 1.2 + (1 / 100 * yt2) - (3 / 100 * yt1) - (4 / 100 * yt1)
        st2 = (3 / 100 * yt1) - (2 / 100 * yt2) - (1 / 100 * yt2)

        return [st1, st2]

    # lijst met timesteps
    t = np.arange(lower_lim, upper_lim, step_size)

    # y-as start waarden voor tank 1 en tank 2
    y0 = [0, 20]

    # y-waarden voor de tanks bij elke x-as stap
    sol = odeint(model, y0, t)

    plt.plot(t, sol[:, 0], 'r', label='tank 1')
    plt.plot(t, sol[:, 1], 'b', label='tank 2')
    plt.xlabel('minuten')
    plt.ylabel('zoutoplossing (kg)')
    plt.legend()
    plt.show()


generate_graph(lower_lim=0, upper_lim=10, step_size=0.001)
