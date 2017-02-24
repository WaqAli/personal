import numpy as np
import sys


class ProjectOne(object):
    def __init__(self, lamda, sigma_sqr, x_train_file, y_train_file):
        self.x_training_data = self.read_x_training(x_train_file)
        self.y_training_data = self.read_y_training(y_train_file)
        self.lamda = lamda
        self.sigma_sqr = sigma_sqr
        self.n_data = self.x_training_data.shape[1]
        self.betas = None

    def read_x_training(self, x_train_file):
        return np.matrix(np.genfromtxt(x_train_file, delimiter=','))

    def read_y_training(self, y_train_file):
        return np.matrix(np.genfromtxt(y_train_file, delimiter=',')).transpose()

    def solve_least_squares_ridge_regression(self):
        XtX_lam = np.dot(self.x_training_data.transpose(), self.x_training_data) + self.lamda * np.identity(self.n_data)
        XtxX_lam_inv = np.linalg.inv(XtX_lam)
        Xty = np.dot(self.x_training_data.transpose(), self.y_training_data)
        self.betas = np.dot(XtxX_lam_inv, Xty)

    def print_betas(self, outfile):
        with open(outfile, 'w') as fp:
            for row in np.nditer(self.betas):
                fp.write(str(row) + '\n')

if __name__ == '__main__':
    args = sys.argv
    filename_lamda = sys.argv[1]
    lamda = float(sys.argv[1])
    sigma_sqr = float(sys.argv[2])
    x_train_file = sys.argv[3]
    y_train_file = sys.argv[4]
    reg = ProjectOne(lamda, sigma_sqr, x_train_file, y_train_file)
    reg.solve_least_squares_ridge_regression()
    reg.print_betas('wRR_{}.csv'.format(filename_lamda))
