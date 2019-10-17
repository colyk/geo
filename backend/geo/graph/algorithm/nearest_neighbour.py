import matplotlib.pyplot as plt
import numpy as np
from numpy import sqrt


class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __repr__(self):
        return "x: %d, y: %d".format(self.x, self.y)


class NearestNeighbourAlgorithm:
    def __init__(self, city_count=10, map_size=(10, 10)):
        self.city_count = city_count
        self.x_size, self.y_size = map_size
        self.X = np.random.uniform(0, self.x_size, self.city_count)
        self.Y = np.random.uniform(0, self.y_size, self.city_count)
        self.way = []
        self.total_distance = None
        self.calculate_optimal_way()

    def calculate_optimal_way(self):
        RS = []
        RW = []
        for city_idx in range(0, self.city_count, 1):
            distance_matrix = self.create_distance_matrix()
            self.way.append(city_idx)
            for i in range(1, self.city_count, 1):
                s = []
                for j in range(0, self.city_count, 1):
                    s.append(distance_matrix[self.way[i - 1], j])

                self.way.append(s.index(min(s)))
                for j in range(0, i, 1):
                    distance_matrix[self.way[i], self.way[j]] = float("inf")
                    distance_matrix[self.way[i], self.way[j]] = float("inf")

            S = sum(
                [
                    self.get_distance_between_cities(i, i + 1)
                    for i in range(0, self.city_count - 1, 1)
                ]
            ) + sqrt(
                (self.X[self.way[self.city_count - 1]] - self.X[self.way[0]]) ** 2
                + (self.Y[self.way[self.city_count - 1]] - self.Y[self.way[0]]) ** 2
            )
            RS.append(S)
            RW.append(self.way)
        self.total_distance = min(RS)
        self.way = RW[RS.index(min(RS))]
        self.X1 = [self.X[self.way[i]] for i in range(0, self.city_count, 1)]
        self.Y1 = [self.Y[self.way[i]] for i in range(0, self.city_count, 1)]

    def generate_random_cities(self):
        return (
            np.random.uniform(0, self.x_size, self.city_count),
            np.random.uniform(0, self.y_size, self.city_count),
        )

    def draw(self):
        plt.title(
            "Distance: %s\nCities: %i"
            % (round(self.total_distance, 3), self.city_count)
        )
        plt.plot(self.X1, self.Y1, color="r", linestyle=" ", marker="o")
        plt.plot(self.X1, self.Y1, color="b", linewidth=1)
        X2 = [self.X[self.way[self.city_count - 1]], self.X[self.way[0]]]
        Y2 = [self.Y[self.way[self.city_count - 1]], self.Y[self.way[0]]]
        plt.plot(
            X2,
            Y2,
            color="g",
            linewidth=2,
            linestyle="-",
            label="Way from last city to first",
        )
        plt.legend(loc="best")
        plt.grid(True)
        plt.show()

    def draw_distances(self):
        Z = sqrt(
            (self.X[self.way[self.city_count - 1]] - self.X[self.way[0]]) ** 2
            + (self.Y[self.way[self.city_count - 1]] - self.Y[self.way[0]]) ** 2
        )
        Y3 = [
            sqrt(
                (self.X[self.way[i + 1]] - self.X[self.way[i]]) ** 2
                + (self.Y[self.way[i + 1]] - self.Y[self.way[i]]) ** 2
            )
            for i in range(0, self.city_count - 1, 1)
        ]
        X3 = [i for i in range(0, self.city_count - 1, 1)]
        plt.title("Distances between cities")
        plt.plot(X3, Y3, color="b", linestyle=" ", marker="o")
        plt.plot(X3, Y3, color="r", linewidth=1, linestyle="-")
        plt.legend(loc="best")
        plt.grid(True)
        plt.show()

    def create_distance_matrix(self):
        empty_matrix = np.zeros([self.city_count, self.city_count])
        for x in np.arange(0, self.city_count, 1):
            for y in np.arange(0, self.city_count, 1):
                empty_matrix[x, y] = (
                    float("inf") if x == y else self.get_distance_between_cities(x, y)
                )
        return empty_matrix

    def get_distance_between_cities(self, x, y):
        return sqrt((self.X[x] - self.X[y]) ** 2 + (self.Y[x] - self.Y[y]) ** 2)


if __name__ == "__main__":
    nna = NearestNeighbourAlgorithm()
    nna.draw()
    nna.draw_distances()
