#! /usr/bin/env python
"""
# File: demo_3d_plot.py
#
# Author: Mike Lum
# Copyright 2021 by the author.
#
# Usage: python -m demo_3d_plot
#
# Description: Plots a 3-d wireframe. Most of the code herein is borrowed from:
#   https://towardsdatascience.com/a-python-tutorial-on-generating-and-plotting-a-3d-guassian-distribution-8c6ec6c41d03
#
# Revision History:
#    Date        Vers.    Author    Description
#   2021-08-06   1.0a1    Lum       New file
#   2021-08-12   1.0f1    Lum       Comments
"""

# Python library imports
from collections import deque
import os
import time

# External library imports
import numpy as np
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D


def bivariate_normal_pdf(domain: float, mean: float, variance: float):
    """
    bivariate_normal_pdf

    Returns a 3-d Gaussian.

    Args:
        domain (float): The neg/pos bound of the axes' range
        mean (float): Gaussian mean
        variance (float): Step size

    Returns:
        x_vals (np.ndarray(float)) : X values of the distribution
        y_vals (np.ndarray(float)) : Y values of the distribution
        z_vals (np.ndarray(float)) : Z values of the distribution

    Raises:
        None
    """
    x_vals = np.arange(-domain+mean, domain+mean, variance)
    y_vals = np.arange(-domain+mean, domain+mean, variance)
    x_vals, y_vals = np.meshgrid(x_vals, y_vals)
    r_vals = np.sqrt(x_vals**2 + y_vals**2)
    z_vals = ((1. / np.sqrt(2 * np.pi)) * np.exp(-.5*r_vals**2))
    return x_vals+mean, y_vals+mean, z_vals


def make_plot(x_vals: np.ndarray, y_vals: np.ndarray, z_vals: np.ndarray,\
              interactive: bool = True) -> None:
    """
    make_plot

    Simple 3-d plot of a parabolic function

    Args:
        x_vals (np.ndarray(float)) : X-coords of the plot
        y_vals (np.ndarray(float)) : Y-coords of the plot
        z_vals (np.ndarray(float)) : Z-coords of the plot
        interactive (bool) : Keep the figure open for interaction

    Returns:
        None

    Raises:
        None
    """
    fig = pyplot.figure(figsize=(12, 6))
    axes = Axes3D(fig, auto_add_to_figure=False)
    fig.add_axes(axes)
    axes.plot_surface(x_vals, y_vals, z_vals,
                      cmap=pyplot.get_cmap("magma"),
                      linewidth=0,
                      antialiased=True)
    axes.set_xlabel('X')
    axes.set_ylabel('Y')
    axes.set_zlabel('Z')
    if interactive:
        pyplot.show()
    else:
        pyplot.show(block=False)


def function_to_test(passes: bool = True) -> bool:
    """
    function_to_test

    Simple function to fake a function to test. Simply returns the passed
    value.

    Args:
        passes (bool): Pass True (or omit) to "pass" the function test.

    Returns:
        (bool): Whether this function passes or not

    Raises:
        None
    """
    print("Running a complex test...")
    time.sleep(3)
    if passes:
        print("The function to test passes!")
    else:
        print("The function to test fails!")

    return passes


if __name__ == '__main__':

    # Parse your command line call - Command line options ignored for now.
    ARGV = deque(os.sys.argv)

    while ARGV:
        FLAG = ARGV.popleft()
        if FLAG == '-test':
            function_to_test(True)
        #else: ...
        # Ignore everything else, or not...

    make_plot(*bivariate_normal_pdf(6, 4, 0.25))
