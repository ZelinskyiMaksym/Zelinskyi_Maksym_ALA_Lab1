import numpy as np
import math


def rotate_xy(X, theta):
    X_copy = X.copy()

    A = np.array([
        [math.cos(theta), -math.sin(theta), 0],
        [math.sin(theta),  math.cos(theta), 0],
        [0,                0,               1]
    ], dtype=float)

    Y = A @ X_copy

    return Y, A


def rotate_xz(X, theta):
    X_copy = X.copy()

    A = np.array([
        [math.cos(theta), 0, -math.sin(theta)],
        [0,               1,                0],
        [math.sin(theta), 0,  math.cos(theta)]
    ], dtype=float)

    Y = A @ X_copy

    return Y, A


def rotate_yz(X, theta):
    X_copy = X.copy()

    A = np.array([
        [1,               0,                0],
        [0, math.cos(theta), -math.sin(theta)],
        [0, math.sin(theta),  math.cos(theta)]
    ], dtype=float)

    Y = A @ X_copy

    return Y, A
