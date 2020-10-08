"""
Метод отжига
"""
import math
import random

import numpy as np


def init_solution(n):
    return np.arange(n)


def tweak_solution(solution):
    solution = np.copy(solution)
    i1 = i2 = 0
    while i1 == i2:
        i1, i2 = np.random.randint(0, len(solution), 2)
    solution[[i1, i2]] = solution[[i2, i1]]
    return solution


def compute_energy(solution):
    n = len(solution)
    board = np.zeros((n, n))
    for x, y in enumerate(solution):
        board[y][x] = 1
    energy = 0
    for x, y in enumerate(solution):
        diag1 = np.diag(board, x-y)
        energy += np.count_nonzero(diag1) - 1
        diag2 = np.diag(board[:, ::-1], n-x-y-1)
        energy += np.count_nonzero(diag2) - 1
    return energy


def emit_solution(solution):
    n = len(solution)
    board = [
        ['#'] * n for _ in range(n)
    ]
    for x, y in enumerate(solution):
        board[y][x] = "Q"
    str_board = "\n".join(
        "".join(row) for row in board
    )
    print(str_board)


if __name__ == "__main__":
    temp_start = 30
    temp_stop = 0.5
    alpha = 0.98
    steps = 1000
    n = 9

    g_bad_decisions = []
    bad_decisions = 0
    g_step = []
    g_temp = []
    g_energy = []

    current_solution = init_solution(n)
    current_energy = compute_energy(current_solution)
    current_temperature = temp_start

    best_solution = np.copy(current_solution)
    best_energy = current_energy

    for step in range(steps):
        if current_temperature <= temp_stop:
            break
        working_solution = tweak_solution(current_solution)
        working_energy = compute_energy(working_solution)
        if working_energy == 0:
            best_solution = np.copy(working_solution)
            best_energy = working_energy
            break
        if working_energy <= current_energy:
            current_temperature *= alpha
            current_solution = working_solution
            current_energy = working_energy
        else:
            threshold = math.exp( -(working_energy - current_energy)/current_temperature )
            if random.random() < threshold:
                current_temperature *= alpha
                current_solution = working_solution
                bad_decisions += 1
        g_step.append(step)
        g_temp.append(current_temperature)
        g_energy.append(current_energy)
        g_bad_decisions.append(bad_decisions)

    emit_solution(best_solution)
    import matplotlib.pyplot as plt
    plt.title("График")
    plt.grid()
    plt.xlabel('Шаги')
    plt.ylabel('Количество')
    plt.plot(g_step, g_temp, label="Температура")
    plt.plot(g_step, g_energy, label="Энергия")
    plt.plot(g_step, g_bad_decisions, label="Плохие решения")
    plt.legend()
    plt.show()







