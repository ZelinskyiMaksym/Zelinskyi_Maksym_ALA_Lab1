import numpy as np


def create_2d_object():
    batman = np.array([
        [0, 0],
        [1, 0.2],
        [0.4, 1],
        [0.5, 0.4],
        [0, 0.8],
        [-0.5, 0.4],
        [-0.4, 1],
        [-1, 0.2],
        [0, 0]
    ], dtype=float)

    return batman.T


def read_off(filename: str):
    with open(filename, 'r') as f:
        # Перевіряємо, чи перший рядок починається з OFF
        if f.readline().strip() != 'OFF':
            raise ValueError('Not a valid OFF header')

        # Зчитуємо кількість вершин, граней та ребер (третє значення часто ігнорується)
        n_verts, n_faces, _ = map(int, f.readline().strip().split())

        # Зчитуємо координати всіх вершин (x, y, z)
        verts = [list(map(float, f.readline().strip().split())) for _ in range(n_verts)]

        # Зчитуємо грані: перше число у рядку - кількість вершин грані (ігноруємо), далі індекси
        faces = [list(map(int, f.readline().strip().split()))[1:] for _ in range(n_faces)]

    # Повертаємо вершини у вигляді масиву NumPy та список граней
    return np.array(verts), faces