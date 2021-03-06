#! /usr/bin/env python
"""
# File: test_distrib.py
#
# Author: Mike Lum
# Copyright 2021 by the author.
#
# Usage: python -m test_distrib
#
# Description: Compares the bivariate normal pdf generated by numpy with one generated using
# PyTorch.
# Most of the code herein is borrowed from:
#   https://towardsdatascience.com/a-python-tutorial-on-generating-and-plotting-a-3d-guassian-distribution-8c6ec6c41d03
#
# Revision History:
#    Date        Vers.    Author    Description
#   2021-08-09   1.0a1    Lum       New file
#   2021-08-12   1.0f1    Lum       Docstrings
"""

# Python library imports
import sys

# External library imports
import numpy as np
import torch

# Internal function to test
sys.path.append('..')   # Necessary for running in tests directory
import demo_3d_plot as d3d


def torch_bivariate_normal_pdf(domain, mean, variance):
    """
    torch_bivariate_normal_pdf

    Calculate a bivariate normal distribution to compare with one using another
    means of calculation

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
    x_vals = torch.arange(-domain+mean, domain+mean, variance)
    y_vals = torch.arange(-domain+mean, domain+mean, variance)
    x_vals, y_vals = torch.meshgrid(x_vals, y_vals)
    ranges = torch.sqrt(x_vals**2 + y_vals**2)
    z_vals = ((1. / np.sqrt(2 * np.pi)) * torch.exp(-.5*ranges**2))
    return x_vals.numpy()+mean, y_vals.numpy()+mean, z_vals.numpy()


def comp_dists(dom, mean, var) -> bool:
    """
    comp_dists

    Compare bivariate normal distributions generated by two different methods.
    This function is intended to verify the demo_3d_plot's bivariate normal
    distribution function.
    It is assumed that the distributions will differ slightly, so this function
    utilizes Numpy's "allclose" function with the default parameters.

    Args:
        domain (float): The neg/pos bound of the axes' range
        mean (float): Gaussian mean
        variance (float): Step size

    Returns:
        success (bool): True if the distributions are the same

    Raises:
        None
    """
    success = True
    test_x, test_y, test_z = d3d.bivariate_normal_pdf(dom, mean, var)
    control_x, control_y, control_z = torch_bivariate_normal_pdf(dom, mean, var)

    print(" # Numerical array validation test #")
    if np.array_equal(test_x, control_x.T):
        print("   X arrays equal")
    elif np.allclose(test_x, control_x.T):
        print("   X arrays close: Max. difference {0:5.3e}".\
              format(np.abs(test_x - control_x).max()))
    else:
        print("   X arrays differ")
        success = False

    if np.array_equal(test_y, control_y.T):
        print("   Y arrays equal")
    elif np.allclose(test_y, control_y.T):
        print("   Y arrays close: Max. difference {0:5.3e}".\
              format(np.abs(test_y - control_y).max()))
    else:
        print("   Y arrays differ")
        success = False

    if np.array_equal(test_z, control_z.T):
        print("   Z arrays equal")
    elif np.allclose(test_z, control_z.T):
        print("   Z arrays close: Max. difference {0:5.3e}".\
              format(np.abs(test_z - control_z).max()))
    else:
        print("   Z arrays differ")
        success = False

    if not success:
        print(" # Numerical array validation test FAILED #")
    else:
        print(" # Numerical array validation test SUCCESS #")

    return success


if __name__ == '__main__':
    if not comp_dists(6, 4, 0.25):
        sys.exit(1)

