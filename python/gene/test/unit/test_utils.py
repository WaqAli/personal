import unittest
import analysis.utils


class TestCorrelation(unittest.TestCase):
    def setUp(self):
        self.x = [1, 2, 3, 4]
        self.y = [4, 3, 2, 1]

    def TearDown(self):
        pass

    def test_correlation_is_one_when_vectors_are_same(self):
        cor_obj = analysis.utils.Correlation(self.x, self.x)
        self.assertEquals(cor_obj.calculate_rho(), -1.0)

    def test_correlation_is_minus_one_when_vectors_are_opposite(self):
        pass

    def test_correlation_is_zero_when_vectors_are_orthogonal(self):
        pass

    def test_exception_is_raised_if_one_vector_is_empty(self):
        pass

    def test_exception_is_raised_if_both_vectors_are_empty(self):
        pass

    def test_exception_is_raised_if_one_vector_is_None(self):
        pass

    def test_exception_is_raised_if_both_vectors_are_None(self):
        pass

    def test_zero_is_returned_if_both_vectors_are_length_one(self):
        pass

    def test_correlation_is_returned_if_nan_present_in_vectors(self):
        pass

