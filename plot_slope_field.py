#!/usr/bin/env python

""" Simple slope field plotter for first-order differential equations
    Takes input as a 2x2 coefficient matrix
"""

import matplotlib.pyplot as plt
import numpy as np
import fire
import sys
from tkinter import Tk, Entry, Button


def plot_field(
    A,
    grid_size=2,
    tick_count=0,
    arrow_density=0.25,
    arrow_color="red",
    gridlines=True,
):
    A = np.array(A)
    xy = np.mgrid[
        -grid_size:grid_size:arrow_density, -grid_size:grid_size:arrow_density,
    ].reshape(2, -1)
    slope = A @ xy
    plt.quiver(*xy, *slope, pivot="middle", color=arrow_color)
    plt.suptitle(str(A))
    if tick_count:
        plt.gca().xaxis.set_ticks(
            np.arange(-grid_size, grid_size, 2 * grid_size / tick_count)
        )
    if gridlines:
        plt.grid()
    plt.show()


def plot_asymptote(A):

    pass


def grab_input(master, A):
    for i in range(2):
        for j in range(2):
            A[i][j] = float(A[i][j].get())
    master.destroy()


def __func_grab_input__(master, A):
    return lambda: grab_input(master, A)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        fire.Fire(plot_field)
    else:
        master = Tk()
        master.title("Plot field")
        A = [
            [Entry(master), Entry(master)],
            [Entry(master), Entry(master)],
        ]
        for i in range(2):
            for j in range(2):
                A[i][j].grid(row=i, column=j)
        button = Button(
            master,
            text="Plot field from matrix",
            command=__func_grab_input__(master, A),
        )
        button.grid(row=2)
        master.mainloop()
        plot_field(A)

