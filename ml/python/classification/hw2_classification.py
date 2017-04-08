import numpy as np
import sys

class ProjectTwo(object):
    def __init__(self, x_train_file, y_train_file, x_test_file):
        self.emp_class_sigma = {}
        self.x_training_data = self.read_x_training(x_train_file)
        self.y_training_data = self.read_y_training(y_train_file)
        self.x_test_data = self.read_x_training(x_test_file)
        self.n_data = self.x_training_data.shape[0]
        self.x_data_dim = self.x_training_data.shape[1]
        self.emp_dist_prior = {}
        self.emp_class_mu = {}


    def read_x_training(self, x_train_file):
        return np.matrix(np.genfromtxt(x_train_file, delimiter=','))

    def read_y_training(self, y_train_file):
        y_data = []
        with open(y_train_file, 'r') as fp:
            for line in fp:
                y_data.append(line.strip())
        return y_data

    def estimates_prior(self):
        for key in range(0, 10):
            self.emp_dist_prior[str(key)] = 0
        total = 0
        for row in self.y_training_data:
            total += 1.0
            self.emp_dist_prior[str(row)] += 1.0

        for key in self.emp_dist_prior:
            self.emp_dist_prior[key] = self.emp_dist_prior[key] / total

    def estimate_class_mu(self):
        for index in range(0, 10):
            self.emp_class_mu[str(index)] = np.zeros((1, self.x_data_dim))
        for index, row in enumerate(self.x_training_data):
            self.emp_class_mu[str(self.y_training_data[index])] += row
        for key in self.emp_class_mu:
            if self.emp_dist_prior[key] > 0:
                self.emp_class_mu[key] = self.emp_class_mu[key] / (self.n_data * self.emp_dist_prior[key])

    def estimate_class_sigma(self):
        for index in range(0, 10):
            self.emp_class_sigma[str(index)] = np.zeros((self.x_data_dim, self.x_data_dim))
        for index, row in enumerate(self.x_training_data):
            self.emp_class_sigma[str(self.y_training_data[index])] += \
                np.dot((row - self.emp_class_mu[str(self.y_training_data[index])]).transpose(),
                       (row - self.emp_class_mu[str(self.y_training_data[index])]))
        for key in self.emp_dist_prior:
            self.emp_class_sigma[key] = (self.emp_class_sigma[key] /
                                                    (self.n_data * self.emp_dist_prior[key]))

    def calculate_posterior(self, y_class, x_new):
        exponent = -0.5 * np.dot(
        np.dot(x_new - self.emp_class_mu[y_class], np.linalg.inv(self.emp_class_sigma[y_class])),
          (x_new - self.emp_class_mu[y_class]).transpose())
        exponent = np.asscalar((exponent))

        posterior = self.emp_dist_prior[y_class] * \
            (np.asscalar(np.linalg.det(self.emp_class_sigma[y_class])) ** -0.5) * \
            np.exp(exponent)
        return posterior

    def generate_output(self, filename):

        fp = open(filename, 'w')
        for x_new_row in self.x_test_data:
            outline = []
            for y_class in range(0, 10):
                outline.append(str(self.calculate_posterior(str(y_class), x_new_row)))
            print >>fp, ','.join(outline)






if __name__ == '__main__':
    args = sys.argv

    x_train_file = sys.argv[1]
    y_train_file = sys.argv[2]
    x_test_file = sys.argv[3]
    cls = ProjectTwo(x_train_file, y_train_file, x_test_file)
    cls.estimates_prior()
    cls.estimate_class_mu()
    cls.estimate_class_sigma()
    cls.generate_output('probs_test.csv')
