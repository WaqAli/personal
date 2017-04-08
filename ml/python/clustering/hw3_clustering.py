import numpy as np
import sys
from scipy.stats import multivariate_normal as normal




class KmeansClustering(object):
    def __init__(self, k, x_data, iter):
        self.x_training_data = self.read_x_training(x_data)
        self.c_assignment = np.zeros(self.x_training_data.shape[0])

        self.n_clusters = k
        self.centroids = self.x_training_data[0: self.n_clusters]
        self.iterations = iter

    def k_means(self):
        for iteration in range(0, self.iterations):
            self.assign_clusters()
            self.calculate_centroids()
            self.print_centroids('centroids-{}.csv'.format(iteration + 1))

    def assign_clusters(self):
        for data_point_index, data_point in enumerate(self.x_training_data):
            min_dist = 100000000000.0
            for cluster_index, centroid in enumerate(self.centroids):
                distance = self.euclidean(data_point, centroid)
                if distance < min_dist:
                    self.c_assignment[data_point_index] = cluster_index
                    min_dist = distance

    def calculate_centroids(self):
        for cluster_index, centroid in enumerate(self.centroids):
            temp_centroid = centroid * 0
            n_points = 0.0
            for data_point_index, data_point in enumerate(self.x_training_data):
                if self.c_assignment[data_point_index] == cluster_index:
                    temp_centroid += data_point
                    n_points +=1
            if n_points > 0:
                self.centroids[cluster_index] = temp_centroid / n_points







    def euclidean(self, x, y):
        return np.power(np.sum(np.power(x-y, 2)), 0.5)



    def read_x_training(self, x_train_file):
        return np.matrix(np.genfromtxt(x_train_file, delimiter=','))


    def print_centroids(self, filename):
        fp = open(filename, 'w')
        for centroid in (self.centroids):
            list = centroid.tolist()
            print >>fp, ','.join(str(i) for i in list[0])


class GaussianMixture(object):
    def __init__(self, clusters, x_data, iterations):

        self.n_clusters = clusters
        self.iterations = iterations
        self.x_training_data = self.read_x_training(x_data)

        self.data_dim = self.x_training_data.shape[1]
        self.n_data = self.x_training_data.shape[0]
        self.mu = self.x_training_data[0: self.n_clusters]
        self.pi = np.zeros(self.n_clusters) + 1.0/self.n_clusters
        self.N = np.zeros(self.n_clusters)
        self.covars = []
        for index in range(0, self.n_clusters):
            self.covars.append(np.identity(self.data_dim, dtype =float))
        self.gamma = np.zeros((self.n_data, self.n_clusters))

    def read_x_training(self, x_train_file):
        return np.matrix(np.genfromtxt(x_train_file, delimiter=','))


    def e_step(self):
        for n in range(0, self.n_data):
            for k in range(0, self.n_clusters):
                self.gamma[n, k] = self.pi[k] * \
                    normal.pdf(self.x_training_data[n], mean=self.mu[k].A1, cov=self.covars[k])

            self.gamma[n] = self.gamma[n] / np.sum(self.gamma[n], axis=0)
    def m_step(self):

        for k in range(0, self.n_clusters):
            mu_new = np.zeros(self.data_dim)
            covar_new = np.zeros((self.data_dim, self.data_dim))
            N = 0
            for n in range(0, self.n_data):
                N = N + self.gamma[n, k]
            self.N[k] = N

            for n in range(0, self.n_data):
                mu_new = mu_new + self.gamma[n, k] * self.x_training_data[n]
            self.mu[k] = mu_new / self.N[k]

            for n in range(0, self.n_data):

                covar_new = covar_new + self.gamma[n, k] * np.dot((self.x_training_data[n].T - self.mu[k].T),
                (self.x_training_data[n].T - self.mu[k].T).T)
            self.covars[k] = covar_new / self.N[k]

            self.pi[k] = self.N[k]/float(self.n_data)

    def run_em(self):
        for iter in range(0, self.iterations):
            self.e_step()
            self.m_step()
            self.print_mu(iter)
            self.print_covars(iter)
            self.print_pi(iter)

    def print_mu(self, iter):
        with open('mu-{}.csv'.format(iter + 1), 'w') as fp:
            for k in range(0, self.n_clusters):
                print >>fp, ','.join(str(num) for num in self.mu[k].A1)


    def print_covars(self, iter):
        for k in range(0, self.n_clusters):
            with open('Sigma-{}-{}.csv'.format(k + 1, iter + 1), 'w') as fp:
                for dim in range(0, self.data_dim):
                    print >>fp, ','.join(str(num) for num in self.covars[k][dim].A1)

    def print_pi(self, iter):
        with open('pi-{}.csv'.format(iter + 1), 'w') as fp:
            for k in range(0, self.n_clusters):
                print >>fp, self.pi[k]


# # # # # # # # # # # # # # # # # #

if __name__ == '__main__':
    x_data = sys.argv[1]

    k_clus = KmeansClustering(5, x_data, 10)
    k_clus.k_means()

    gm = GaussianMixture(5, x_data, 10)
    gm.run_em()



