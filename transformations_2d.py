import numpy as np
import math


def stretch(X, a, b):
    X_copy = X.copy()
    A = np.array([
        [a, 0],
        [0, b]
    ], dtype=float)

    Y = A @ X_copy

    return Y, A


def shear(X, a, b):
    X_copy = X.copy()
    A = np.array([
        [1, a],
        [b, 1]
    ], dtype=float)

    Y = A @ X_copy

    return Y, A


def reflection(X, a, b):
    X_copy = X.copy()
    A = np.array([
        [a**2 - b**2, 2*a*b],
        [2*a*b, b**2 - a**2]
    ], dtype=float) / (a**2 + b**2)

    Y = A @ X_copy

    return Y, A


def rotation(X, theta):
    X_copy = X.copy()
    A = np.array([
        [math.cos(theta), -(math.sin(theta))],
        [math.sin(theta), math.cos(theta)]
    ], dtype=float)

    Y = A @ X_copy

    return Y, A