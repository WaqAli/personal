import numpy as np
import math


def mean(vector_x):
    assert (vector_x is not None)
    return np.sum(vector_x) / len(vector_x)


class Correlation(object):
    def __init__(self, vector_x, vector_y):
        self.x = np.array(vector_x, dtype=float)
        self.y = np.array(vector_y, dtype=float)

    def calculate_rho_using_numpy(self):
        return np.corrcoef(self.x, self.y)

    def calculate_rho(self):
        assert (self.x is not None and self.y is not None)
        rho = np.sum((self.x - mean(self.x)) * (self.y - mean(self.y))) / \
            np.sqrt(np.sum((self.x - mean(self.x))**2) * np.sum((self.y - mean(self.y))**2))
        return rho






class MatrixInversion(object):
    pass


class MatrixTranspose(object):
    pass


class MatrixMultiplication(object):
    pass

