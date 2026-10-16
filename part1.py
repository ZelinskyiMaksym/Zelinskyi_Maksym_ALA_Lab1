from data import create_2d_object
from transformations_2d import stretch, shear, reflection, rotation
from visualization import plot_2d
import numpy as np
import math


def run_task1():
    print("\nTask 1")
    X = create_2d_object()

    line_color_for_Y = "blue"
    point_color_for_Y = "red"

    plot_2d(X)

    # Розтягнення
    Y, A = stretch(X, 2, 0.5)

    print("Stretch matrix:")
    print(A)

    plot_2d(Y, line_color_for_Y, point_color_for_Y)

    # Зсув
    Y, A = shear(X, 1, 0)

    print("Shear matrix:")
    print(A)

    plot_2d(Y, line_color_for_Y, point_color_for_Y)

    # Відбиття
    Y, A = reflection(X, 1, 0)

    print("Reflection matrix:")
    print(A)

    plot_2d(Y, line_color_for_Y, point_color_for_Y)

    # Поворот
    Y, A = rotation(X, math.pi / 2)

    print("Rotation matrix:")
    print(A)

    plot_2d(Y, line_color_for_Y, point_color_for_Y)

    # У Stretch при a=2, b=1 ширина збільшилась удвічі, висота не змінилась.
    # При a=1, b=2 навпаки — збільшилась лише висота.
    # Значення 0.5 зменшує відповідний розмір удвічі.
    # У Shear зміна a дає горизонтальний зсув, зміна b — вертикальний.
    # Reflection з (1, 0) перевернуло фігуру відносно осі x,
    # а з (1, 1) — відносно прямої y=x.
    # Для (1, 2) і (2, 4) результат однаковий, бо пряма та сама.
    # В Rotation зміна знака кута змінила напрям повороту, розміри збереглись.


def run_task2():
    print("\nTask 2")
    X = create_2d_object()

    line_color_for_Y = "blue"
    point_color_for_Y = "red"

    plot_2d(X)

    # Базова послідовність
    print("Basic order")

    Y, S = stretch(X, 2, 0.5)

    print("Stretch matrix:")
    print(S)

    plot_2d(Y, line_color_for_Y, point_color_for_Y)

    Y, H = shear(Y, 1, 0)

    print("Shear matrix:")
    print(H)
    plot_2d(Y, line_color_for_Y, point_color_for_Y)

    Y, R = rotation(Y, math.pi / 4)

    print("Rotation matrix:")
    print(R)
    plot_2d(Y, line_color_for_Y, point_color_for_Y)

    A = R @ H @ S

    print("Total transformation matrix:")
    print(A)

    # Змінені порядки
    orders = [
        ["Shear", "Stretch", "Rotation"],
        ["Rotation", "Shear", "Stretch"],
        ["Stretch", "Rotation", "Shear"]
    ]

    for order in orders:
        print("\nOrder:", order)

        Y = X.copy()
        A_total = np.eye(2)

        for transformation in order:
            if transformation == "Stretch":
                Y, A = stretch(Y, 2, 0.5)

            elif transformation == "Shear":
                Y, A = shear(Y, 1, 0)

            elif transformation == "Rotation":
                Y, A = rotation(Y, math.pi / 4)

            A_total = A @ A_total

            print(transformation)
            print(A)

            plot_2d(Y, line_color_for_Y, point_color_for_Y)

        print("Total transformation matrix:")
        print(A_total)

    # Параметри залишались однаковими,
    # але після зміни порядку отримав різні кінцеві фігури.
    # Отже, результат залежить від порядку перетворень.