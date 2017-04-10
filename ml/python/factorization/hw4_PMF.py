import sys
import numpy as np
import scipy.stats as ss
import math


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
        self.iterations = 50
        self.L = None
        self.I = np.identity(self.dim)

    def read_input(self, filename):
        with open(filename, 'r') as fp:
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
                self.objects[object] = 1
                self.M[str(user) + ':' + str(object)] = ranking
            self.U = np.matrix(np.ndarray((max_user+1, self.dim)) * 0)
            self.V = np.matrix(np.ndarray((max_object+1, self.dim)) * 0)

    def initialize_objects(self):
        for index in self.objects:
            self.V[int(index)] = np.random.multivariate_normal(mean=np.zeros(self.dim), cov=(self.lamda**-1)*self.I)

    def initialize_users(self):
        for index in self.users:
            self.U[int(index)] = np.random.multivariate_normal(mean=np.zeros(self.dim), cov=(self.lamda ** -1) * self.I)

    def update_users(self):
        for user in self.users:
            self.U[int(user)] = (np.linalg.inv(self.lamda*self.sigma_sqr*self.I + self.sum_vv(user)) \
            * self.sum_Mv(user)).transpose()

    def update_objects(self):
        for obj in self.objects:
            self.V[int(obj)] = (np.linalg.inv(self.lamda * self.sigma_sqr * self.I + self.sum_uu(obj)) \
                                * self.sum_Mu(obj)).transpose()


    def sum_Mv(self, i):
        summation = np.matrix(np.zeros((self.dim, 1)))
        for index in self.objects:
            if str(i) + ':' + str(index) in self.M:
                summation = summation + self.M[str(i) + ':' + str(index)] * self.V[int(index)].transpose()
        return summation

    def sum_Mu(self, i):
        summation = np.matrix(np.zeros((self.dim, 1)))
        for index in self.users:
            if (str(index) + ':' + str(i)) in self.M:
                summation = summation + self.M[str(index) + ':' + str(i)] * self.U[int(index)].transpose()
        return summation

    def sum_vv(self, user):
        sum = 0.0
        for index in self.objects:
            if (str(user) + ':' + str(index)) in self.M:
                sum = sum + (self.V[int(index)].transpose() * self.V[int(index)])
        return sum

    def sum_uu(self, obj):
        sum = 0.0
        for index in self.users:
            if (str(index) + ':' + str(obj)) in self.M:
                sum = sum + (self.U[int(index)].transpose() * self.U[int(index)])
        return sum


    def calculate_likelihood(self):
        first_sum = 0.0
        for key in self.M:
            user = int(key.split(':')[0])
            obj = int(key.split(':')[1])
            first_sum += (self.M[key] - (self.U[user]*self.V[obj].transpose()))**2/(2*self.sigma_sqr)

        second_sum = 0.0
        for user in self.users:
            second_sum += np.linalg.norm(self.U[int(user)]) * self.lamda/2

        third_sum = 0.0
        for obj in self.objects:
            third_sum += np.linalg.norm(self.V[int(obj)]) * self.lamda / 2

        self.L = (0 - first_sum - second_sum - third_sum)[0,0]






    def output_matrices(self, iteration):
        with open('V-{}.csv'.format(iteration), 'w') as fp:
            for obj in self.objects:
                obj_rankings = ','.join([str(number) for number in self.V[int(obj)].tolist()[0]])
                print >> fp, obj_rankings


        with open('U-{}.csv'.format(iteration), 'w') as fp:
            for user in self.users:
                user_rankings = ','.join([str(number) for number in self.U[int(user)].tolist()[0]])
                print >>fp, user_rankings

    def output_likelihood(self, iteration):
        with open('objective.csv', 'a') as fp:
            print >> fp, self.L
            print iteration, self.L


    def run_pmf(self):
        for iteration in range(1, self.iterations + 1):
            self.update_users()
            self.update_objects()
            self.calculate_likelihood()
            if iteration in [10, 25, 50]:
                self.output_matrices(iteration)
            self.output_likelihood(iteration)






if __name__ == '__main__':
    pmf = PMF()
    pmf.read_input(sys.argv[1])


    pmf.initialize_objects()

    pmf.run_pmf()
