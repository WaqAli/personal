import sys
import numpy as np
import scipy.stats as ss


class PMF(object):
    def __init__(self):
        self.users = {}
        self.objects = {}
        self.M = {}
        self.V = None
        self.U = None
        self.dim = 5
        self.lamda = 2
        self.sigma_sqr = 0.1
        self.I = np.identity(self.dim)

    def read_input(self, filename):
        with open(filename) as fp:
            max_user = 0
            max_object = 0
            for line in fp:
                user, object, ranking = line.split(',')
                user = int(user)
                object = int(object)
                ranking = float(ranking)
                if user > max_user:
                    max_user = user
                if object > max_object:
                    max_object = object
                self.users[user] = 1
                self.objects[object] =1
                self.M[str(user) + ':' + str(object)] = ranking
            self.U = np.ndarray((max_user, self.dim)) * 0
            self.V = np.ndarray((max_object, self.dim)) * 0

    def initialize_objects(self):
        for index in self.objects:
            self.V[int(index)] = np.random.multivariate_normal(mean=np.zeros(self.dim), cov=(self.lamda**-1)*self.I)


if __name__ == '__main__':
    pmf = PMF()
    pmf.read_input(sys.argv[1])
    pmf.initialize_objects()
    print pmf.V
