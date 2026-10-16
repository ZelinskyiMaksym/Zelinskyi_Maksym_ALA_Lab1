from data import read_off
from transformations_3d import rotate_xy, rotate_yz, rotate_xz
from visualization import plot_off
import math


def run_task3():
    print("\nTask 3")
    vertices, faces = read_off("data/models/model.off")

    plot_off(vertices, faces)

    X = vertices.T

    # Поворот XY
    Y, A = rotate_xy(X, math.pi / 4)

    print("XY rotation matrix:")
    print(A)

    plot_off(Y.T, faces)

    # Поворот XZ
    Y, A = rotate_xz(X, math.pi / 4)

    print("XZ rotation matrix:")
    print(A)

    plot_off(Y.T, faces)

    # Поворот YZ
    Y, A = rotate_yz(X, math.pi / 4)

    print("YZ rotation matrix:")
    print(A)

    plot_off(Y.T, faces)


def run_task4():
    print("\nTask 4")
    vertices, faces = read_off("data/models/model.off")

    X = vertices.T

    Y, A_xy = rotate_xy(X, math.pi / 4)

    Y, A_yz = rotate_yz(Y, math.pi / 4)

    Y, A_xz = rotate_xz(Y, math.pi / 4)

    A_total = A_xz @ A_yz @ A_xy

    print("Total rotation matrix:")
    print(A_total)

    plot_off(Y.T, faces)