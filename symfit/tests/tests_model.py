from __future__ import division, print_function
import unittest
import warnings
import types

import sympy
import numpy as np
from scipy.optimize import curve_fit

from symfit import Variable, Parameter, Fit, FitResults, LinearLeastSquares, parameters, variables, NumericalLeastSquares, NonLinearLeastSquares, Model, TaylorModel
from symfit.core.support import seperate_symbols, sympy_to_py
from symfit.distributions import Gaussian


class TestModel(unittest.TestCase):
    """
    Tests for Model objects.
    """
    def test_model_as_dict(self):
        x, y_1, y_2 = variables('x, y_1, y_2')
        a, b = parameters('a, b')

        model_dict = {y_1: a * x**2, y_2: 2 * x * b}
        model = Model.from_dict(model_dict)

        self.assertEqual(id(model[y_1]), id(model_dict[y_1]))
        self.assertEqual(id(model[y_2]), id(model_dict[y_2]))
        self.assertEqual(len(model), len(model_dict))
        self.assertEqual(model.items(), model_dict.items())
        self.assertTrue(y_1 in model)
        self.assertFalse(model[y_1] in model)


if __name__ == '__main__':
    unittest.main()
