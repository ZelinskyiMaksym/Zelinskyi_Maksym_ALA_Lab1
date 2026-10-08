import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


MODEL_FILE = Path(__file__).with_name("model.off")


def stretch(X, a, b):
    X_copy = X.copy()
    A = np.array([
        [a, 0],
        [0, b]
    ], dtype=float)
    Y = A @ X_copy
    print("Stretch matrix:")
    print(A)
    return Y


def shear(X, a, b):
    X_copy = X.copy()
    A = np.array([[1, a], [b, 1]], dtype=float)
    Y = A @ X_copy
    print("Shear matrix:")
    print(A)
    return Y


def reflection(X, a, b):
    if a == 0 and b == 0:
        raise ValueError("Вектор напрямку прямої не може бути нульовим.")
    X_copy = X.copy()
    A = np.array([
        [a**2 - b**2, 2 * a * b],
        [2 * a * b, b**2 - a**2],
    ], dtype=float) / (a**2 + b**2)
    Y = A @ X_copy
    print("Reflection matrix:")
    print(A)
    return Y


def rotation(X, theta):
    X_copy = X.copy()
    c, s = math.cos(theta), math.sin(theta)
    A = np.array([[c, -s], [s, c]], dtype=float)
    Y = A @ X_copy
    print("Rotation matrix:")
    print(A)
    return Y


def plot_2d(arrays, titles, heading):
    fig, axes = plt.subplots(
        1, len(arrays), figsize=(3.5 * len(arrays), 4.5),
        sharex=True, sharey=True,
    )
    all_points = np.concatenate(arrays, axis=1)
    lower = np.minimum(all_points.min(axis=1), 0)
    upper = np.maximum(all_points.max(axis=1), 0)
    padding = 0.08 * max(float(np.max(upper - lower)), 1.0)

    for index, (ax, data, title) in enumerate(zip(axes, arrays, titles)):
        ax.plot(data[0], data[1], "o-", color="blue" if index == 0 else "red")
        ax.set_title(title)
        ax.set_xlim(lower[0] - padding, upper[0] + padding)
        ax.set_ylim(lower[1] - padding, upper[1] + padding)
        ax.set_aspect("equal", adjustable="box")
        ax.axhline(0, color="gray", linewidth=0.8)
        ax.axvline(0, color="gray", linewidth=0.8)
        ax.grid(True)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
    fig.suptitle(heading)
    fig.tight_layout()
    return fig


def task_1(X):
    print("\nTask1")
    examples = [
        (1, 4, 2, 4, 1, 4, 90),
        (1.5, 0.7, 0.5, 0, 1, 1, 45),
    ]
    for number, (a, b, c, d, u, v, degrees) in enumerate(examples, start=1):
        print(f"\nVar {number}:")
        arrays = [
            X, stretch(X, a, b), shear(X, c, d),
            reflection(X, u, v), rotation(X, math.radians(degrees)),
        ]
        titles = [
            "Original", f"Stretch: a={a}, b={b}",
            f"Shear: a={c}, b={d}",
            f"Reflection: direction ({u}, {v})", f"Rotation: {degrees} deg",
        ]
        plot_2d(arrays, titles, f"Task 1: var {number}")


def task_2(X):
    print("\nTask2")
    a, b = 1, 4
    c, d = 2, 4
    theta = math.radians(90)

    operations = {
        "Stretch": lambda data: stretch(data, a, b),
        "Shear": lambda data: shear(data, c, d),
        "Rotation": lambda data: rotation(data, theta),
    }
    cosine, sine = math.cos(theta), math.sin(theta)
    matrices = {
        "Stretch": np.array([[a, 0], [0, b]], dtype=float),
        "Shear": np.array([[1, c], [d, 1]], dtype=float),
        "Rotation": np.array([[cosine, -sine], [sine, cosine]], dtype=float),
    }
    orders = [
        ("Shear", "Stretch", "Rotation"),
        ("Stretch", "Shear", "Rotation"),
        ("Rotation", "Stretch", "Shear"),
        ("Shear", "Rotation", "Stretch"),
    ]
    results = []

    for order in orders:
        print("\nПорядок: " + " -> ".join(order))
        current = X.copy()
        arrays = [X]
        titles = ["Original"]
        composite = np.eye(2)
        for step, name in enumerate(order, start=1):
            current = operations[name](current)
            composite = matrices[name] @ composite
            arrays.append(current.copy())
            titles.append(f"Step {step}: {name}")

        print("Матриця всієї композиції (останнє перетворення стоїть зліва):")
        print(composite)
        print("Кінцеві координати:")
        print(current)
        results.append(current.copy())
        plot_2d(arrays, titles, "Task 2: " + " -> ".join(order))

    print("\nПорівняння кінцевих результатів:")
    for i in range(len(results)):
        for j in range(i + 1, len(results)):
            same = np.allclose(results[i], results[j])
            print(f"Порядки {i + 1} та {j + 1}: " + ("однакові" if same else "різні"))
    print("Висновок: У загальному випадку  матриці не комутативні: A @ B не рівне B @ A.")


def read_off(filename):
    with open(filename, "r", encoding="utf-8-sig") as f:
        def next_line():
            for line in f:
                line = line.split("#", 1)[0].strip()
                if line:
                    return line
            raise ValueError("OFF-файл закрився.")

        header = next_line().split()
        if header[0] != "OFF":
            raise ValueError("Немає OFF.")
        counts = header[1:] or next_line().split()
        if len(counts) < 3:
            raise ValueError("Немає кількості вершин, граней і ребер.")
        n_vertices, n_faces, n_edges = map(int, counts[:3])
        if n_vertices <= 0 or n_faces < 0 or n_edges < 0:
            raise ValueError("Неправильна кількість вершин, граней або ребер.")

        vertices = []
        for _ in range(n_vertices):
            xyz = list(map(float, next_line().split()[:3]))
            if len(xyz) != 3 or not all(math.isfinite(value) for value in xyz):
                raise ValueError("Кожна вершина повинна мати три скінченні координати.")
            vertices.append(xyz)

        faces = []
        for _ in range(n_faces):
            values = next_line().split()
            count = int(values[0])
            face = list(map(int, values[1:count + 1]))
            if count < 3 or len(face) != count:
                raise ValueError("Некоректна грань у OFF-файлі.")
            if any(index < 0 or index >= n_vertices for index in face):
                raise ValueError("Грань містить неіснуючу вершину.")
            faces.append(face)
    return np.array(vertices, dtype=float), faces


def plot_off(vertices, faces, title, ax, limits):
    if faces:
        mesh = Poly3DCollection(
            [vertices[face] for face in faces],
            alpha=0.3, facecolor="skyblue", edgecolor="k", linewidth=0.2,
        )
        ax.add_collection3d(mesh)
    ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], s=2, c="r")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title(title)
    ax.set_xlim(*limits[0])
    ax.set_ylim(*limits[1])
    ax.set_zlim(*limits[2])
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=25, azim=35)

def rotate_xy(X, theta):
    X_copy = X.copy()
    c, s = math.cos(theta), math.sin(theta)
    A = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], dtype=float)
    Y = A @ X_copy
    print("\nRotation XY matrix:")
    print(A)
    return Y


def rotate_yz(X, theta):
    X_copy = X.copy()
    c, s = math.cos(theta), math.sin(theta)
    A = np.array([[1, 0, 0], [0, c, -s], [0, s, c]], dtype=float)
    Y = A @ X_copy
    print("\nRotation YZ matrix:")
    print(A)
    return Y


def rotate_xz(X, theta):
    X_copy = X.copy()
    c, s = math.cos(theta), math.sin(theta)
    # Знаки sin(theta) відповідають саме формулі XZ з PDF лабораторної.
    A = np.array([[c, 0, -s], [0, 1, 0], [s, 0, c]], dtype=float)
    Y = A @ X_copy
    print("\nRotation XZ matrix:")
    print(A)
    return Y


def task_3(filename):
    print("Task3")
    vertices, faces = read_off(filename)
    X = vertices.T
    degrees = 45
    theta = math.radians(degrees)


    models = [vertices, rotate_xy(X, theta).T,
              rotate_yz(X, theta).T, rotate_xz(X, theta).T]
    titles = ["Original", f"XY rotation: {degrees} deg",
              f"YZ rotation: {degrees} deg", f"XZ rotation: {degrees} deg"]

    all_vertices = np.concatenate(models, axis=0)
    lower = all_vertices.min(axis=0)
    upper = all_vertices.max(axis=0)
    center = (lower + upper) / 2
    half_span = 0.55 * max(float(np.max(upper - lower)), 1e-9)
    limits = [(value - half_span, value + half_span) for value in center]

    fig = plt.figure(figsize=(12, 10))
    for index, (model, title) in enumerate(zip(models, titles), start=1):
        ax = fig.add_subplot(2, 2, index, projection="3d")
        plot_off(model, faces, title, ax, limits)
    fig.suptitle("Task 3: three separate 3D rotations")
    fig.tight_layout(pad=2)
    return models


def main():
    np.set_printoptions(precision=4, suppress=True)
    points = np.array([
        [0, 0], [3, 0], [3, 1], [1, 2], [0, 1], [0, 0],
    ], dtype=float)
    X = points.T
    task_1(X)
    task_2(X)

    if MODEL_FILE.is_file():
        task_3(MODEL_FILE)
        # ===== Завдання 4: композиція трьох 3D-поворотів =====
        angle_xy = 45
        angle_yz = 30
        angle_xz = 60

        if MODEL_FILE.is_file():
            vertices, faces = read_off(MODEL_FILE)
            X = vertices.T.copy()

            alpha = math.radians(angle_xy)
            beta = math.radians(angle_yz)
            gamma = math.radians(angle_xz)

            # Матриця повороту в площині XY.
            A_xy = np.array([
                [math.cos(alpha), -math.sin(alpha), 0],
                [math.sin(alpha), math.cos(alpha), 0],
                [0, 0, 1]
            ], dtype=float)

            # Матриця повороту в площині YZ.
            A_yz = np.array([
                [1, 0, 0],
                [0, math.cos(beta), -math.sin(beta)],
                [0, math.sin(beta), math.cos(beta)]
            ], dtype=float)

            # Матриця повороту в площині XZ за формулою лабораторної.
            A_xz = np.array([
                [math.cos(gamma), 0, -math.sin(gamma)],
                [0, 1, 0],
                [math.sin(gamma), 0, math.cos(gamma)]
            ], dtype=float)

            # Послідовність: XY -> YZ -> XZ.
            Z = A_xy @ X
            Y = A_yz @ Z
            V = A_xz @ Y

            # Матриця всієї композиції.
            A = A_xz @ A_yz @ A_xy

            print("\nTask 4 — composition matrix:")
            print(A)

            # Початкова модель і кінцевий результат.
            models = [vertices, V.T]
            titles = [
                "Original",
                f"XY {angle_xy}° -> YZ {angle_yz}° -> XZ {angle_xz}°"
            ]

            # Спільні межі та однаковий масштаб осей.
            all_vertices = np.concatenate(models, axis=0)
            lower = all_vertices.min(axis=0)
            upper = all_vertices.max(axis=0)
            center = (lower + upper) / 2
            half_span = 0.55 * max(float(np.max(upper - lower)), 1e-9)
            limits = [(value - half_span, value + half_span)
                      for value in center]

            fig = plt.figure(figsize=(12, 6))

            for index, (model, title) in enumerate(zip(models, titles), 1):
                ax = fig.add_subplot(1, 2, index, projection="3d")
                plot_off(model, faces, title, ax, limits)

            fig.suptitle("Task 4: composition of 3D rotations")
            fig.tight_layout(pad=2)
    else:
        print(f"\nНе знайдено OFF-модель: {MODEL_FILE}")
        print("Для завдання 3 поклади model.off із ModelNet40 поруч із програмою.")
        print("Або зміни MODEL_FILE на шлях до своєї OFF-моделі.")
    plt.show()


if __name__ == "__main__":
    main()