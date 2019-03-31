""""Nearest neighbour algorithm"""

import matplotlib.pyplot as plt
import numpy as np
from numpy import sqrt


CITY_COUNT = 5
map_size = 100
way = []

X = np.random.uniform(0, map_size, CITY_COUNT)
Y = np.random.uniform(0, map_size, CITY_COUNT)

RS = []
RW = []
RIB = []
s = []


def get_distance_between_cities(i, j):
    return sqrt((X[i] - X[j]) ** 2 + (Y[i] - Y[j]) ** 2)


def create_distance_matrix():
    empty_matrix = np.zeros([CITY_COUNT, CITY_COUNT])
    for i in np.arange(0, CITY_COUNT, 1):
        for j in np.arange(0, CITY_COUNT, 1):
            if i != j:
                empty_matrix[i, j] = get_distance_between_cities(i, j)
            else:
                empty_matrix[i, j] = float('inf')
    return empty_matrix


for city_index in np.arange(0, CITY_COUNT, 1):
    distance_matrix = create_distance_matrix()
    way.append(city_index)
    for i in np.arange(1, CITY_COUNT, 1):
        s = []
        for j in np.arange(0, CITY_COUNT, 1):
            s.append(distance_matrix[way[i - 1], j])
        way.append(s.index(min(s)))
        for j in np.arange(0, i, 1):
            distance_matrix[way[i], way[j]] = float('inf')
            distance_matrix[way[i], way[j]] = float('inf')

    S = sum([sqrt((X[way[i]] - X[way[i + 1]]) ** 2 + (Y[way[i]] - Y[way[i + 1]]) ** 2)
             for i in np.arange(0, CITY_COUNT - 1, 1)]) + sqrt(
        (X[way[CITY_COUNT - 1]] - X[way[0]]) ** 2 + (Y[way[CITY_COUNT - 1]] - Y[way[0]]) ** 2)
    RS.append(S)
    RW.append(way)
    RIB.append(city_index)
S = min(RS)
way = RW[RS.index(min(RS))]
city_index = RIB[RS.index(min(RS))]

X1 = [X[way[i]] for i in np.arange(0, CITY_COUNT, 1)]
Y1 = [Y[way[i]] for i in np.arange(0, CITY_COUNT, 1)]


def draw_map():
    plt.title('Общий путь-%s.Номер города-%i.Всего городов -%i.\n Координаты X,Y заданы' %
              (round(S, 3), city_index, CITY_COUNT), size=14)
    plt.plot(X1, Y1, color='r', linestyle=' ', marker='o')
    plt.plot(X1, Y1, color='b', linewidth=1)
    X2 = [X[way[CITY_COUNT - 1]], X[way[0]]]
    Y2 = [Y[way[CITY_COUNT - 1]], Y[way[0]]]
    plt.plot(X2, Y2, color='g', linewidth=2, linestyle='-',
             label='Путь от  последнего \n к первому городу')
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()


def draw_distances():
    Z = sqrt((X[way[CITY_COUNT - 1]] - X[way[0]]) ** 2 +
             (Y[way[CITY_COUNT - 1]] - Y[way[0]]) ** 2)
    Y3 = [sqrt((X[way[i + 1]] - X[way[i]]) ** 2 + (Y[way[i + 1]] - Y[way[i]]) ** 2)
          for i in np.arange(0, CITY_COUNT - 1, 1)]
    X3 = [i for i in np.arange(0, CITY_COUNT - 1, 1)]
    plt.title('Пути от города к городу')
    plt.plot(X3, Y3, color='b', linestyle=' ', marker='o')
    plt.plot(X3, Y3, color='r', linewidth=1, linestyle='-',
             label='Без учёта замыкающего пути - %s' % str(round(Z, 3)))
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    draw_map()
    draw_distances()
