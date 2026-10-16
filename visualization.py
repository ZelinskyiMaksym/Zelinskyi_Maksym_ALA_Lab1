import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def plot_2d(X, line_color="black", point_color="red"):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1)

    ax.plot(X[0], X[1], color=line_color)

    ax.scatter(X[0], X[1], s=2, color=point_color)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    ax.set_aspect("equal")

    plt.show()


def plot_off(vertices, faces):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    mesh = Poly3DCollection([vertices[face] for face in faces],
                            alpha=0.3, edgecolor='black')
    ax.add_collection3d(mesh)

    ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], s=2, color='red')

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    ax.auto_scale_xyz(vertices[:, 0], vertices[:, 1], vertices[:, 2])

    plt.show()