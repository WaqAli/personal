import unittest
import analysis.utils
import numpy as np


class TestCorrelation(unittest.TestCase):

    def test_correlation_is_one_when_vectors_are_same(self):
        vector_x = [1, 2, 3, 4]
        vector_y = [1, 2, 3, 4]
        cor_obj = analysis.utils.Correlation(vector_x, vector_y)
        self.assertEquals(cor_obj.calculate_rho(), 1.0)

    def test_correlation_is_minus_one_when_vectors_are_opposite(self):
        vector_x = [1, 2, 3, 4]
        vector_y = [-1, -2, -3, -4]
        cor_obj = analysis.utils.Correlation(vector_x, vector_y)
        self.assertEquals(cor_obj.calculate_rho(), -1.0)

    def test_exception_is_raised_if_one_vector_is_empty(self):
        vector_x = [1, 2, 3, 4]
        vector_y = []
        self.assertRaises(AssertionError, analysis.utils.Correlation(vector_x, vector_y).calculate_rho)

    def test_exception_is_raised_if_both_vectors_are_empty(self):
        vector_x = []
        vector_y = []
        self.assertRaises(AssertionError, analysis.utils.Correlation(vector_x, vector_y).calculate_rho)

    def test_exception_is_raised_if_one_vector_is_None(self):
        vector_x = [1, 2, 3, 4]
        vector_y = None
        self.assertRaises(AssertionError, analysis.utils.Correlation(vector_x, vector_y).calculate_rho)

    def test_exception_is_raised_if_both_vectors_are_None(self):
        vector_x = None
        vector_y = None
        self.assertRaises(AssertionError, analysis.utils.Correlation(vector_x, vector_y).calculate_rho)

    def test_exception_is_raised_if_both_vectors_are_length_one(self):
        vector_x = [1]
        vector_y = [1]
        self.assertRaises(AssertionError, analysis.utils.Correlation(vector_x, vector_y).calculate_rho)

    def test_nan_is_returned_if_nan_present_in_one_vector(self):
        vector_x = [1, 2, np.nan, 4]
        vector_y = [-1, -2, -3, -4]
        cor_obj = analysis.utils.Correlation(vector_x, vector_y)
        self.assertTrue(np.isnan(cor_obj.calculate_rho()))


class TestMean(unittest.TestCase):
    def test_should_return_mean_when_all_values_are_same(self):
        vector_x = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.assertEquals(analysis.utils.mean(vector_x), 1.0)

    def test_should_return_nan_when_vector_is_empty(self):
        vector_x = []
        self.assertTrue(np.isnan(analysis.utils.mean(vector_x)))

    def test_should_return_nan_when_vector_contains_nan(self):
        vector_x = [1, 1, 1, 1, 1, 1, 1, 1, np.nan, 1]
        self.assertTrue(np.isnan(analysis.utils.mean(vector_x)))

    def test_should_fail(self):
        self.fail()


if __name__ == "__main__":
    unittest.main()