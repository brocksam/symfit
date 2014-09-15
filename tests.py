import unittest
import sympy
from sympy import symbols
import numpy as np
from symfit.api import Variable, Parameter, Minimize, Fit, FitResults


class TddInPythonExample(unittest.TestCase):
    def test_gaussian(self):
        x0 = Parameter('x0')
        sig = Parameter('sig')
        x = Variable('x')
        new = sympy.exp(-(x - x0)**2/(2*sig**2))
        self.assertIsInstance(new, sympy.exp)

    def test_fitting(self):
        xdata = np.linspace(1,10,10)
        ydata = 3*xdata**2

        a = Parameter('a')
        b = Parameter('b')
        x = Variable('x')
        new = a*x**b

        fit = Fit(new, xdata, ydata)

        result = fit.scipy_func(fit.xdata, 2, 3)
        self.assertTrue(np.array_equal(result, np.array([2., 16., 54., 128., 250., 432., 686., 1024., 1458., 2000.])))

        import inspect
        args, varargs, keywords, defaults = inspect.getargspec(fit.scipy_func)

        # self.assertEqual(args, ['x', 'a', 'b'])
        fit_result = fit.execute()
        self.assertIsInstance(fit_result, FitResults)
        print(fit_result)

    def test_numpy_functions(self):
        xdata = np.linspace(1,10,10)
        ydata = 45*np.log(xdata*2)

        a = Parameter('a')
        b = Parameter('b', value=2.1, fixed=True)
        x = Variable('x')
        new = a*sympy.log(x*b)

        fit = Fit(new, xdata, ydata)
        fit_result = fit.execute()
        print(fit_result.popt)

    def test_2D_fitting(self):
        xdata = np.random.randint(-10,11,size=(2,400))
        zdata = 2.5*xdata[0]**2 + 7.0*xdata[1]**2

        a = Parameter('a')
        b = Parameter('b')
        x = Variable('x')
        y = Variable('y')
        new = a*x**2 + b*y**2

        fit = Fit(new, xdata, zdata)

        result = fit.scipy_func(fit.xdata, 2, 3)

        import inspect
        args, varargs, keywords, defaults = inspect.getargspec(fit.scipy_func)

        self.assertEqual(args, ['x', 'a', 'b'])
        fit_result = fit.execute()
        print fit_result.params, fit_result.popt, fit_result.pcov
        self.assertIsInstance(fit_result, FitResults)

    def test_minimize(self):
        x = Variable()
        y = Variable()
        model = 2*x*y + 2*x - x**2 - 2*y**2
        from sympy import Eq
        constraints = [
            x**3 - y == 0,
            y - 1 >= 0,
        ]
        print(type(x**3 - y))
        print x**3 - y == 0.0
        self.assertIsInstance(constraints[0], Eq)

        fit = Minimize(model, constraints=constraints)
        fit_result = fit.execute()
        self.assertAlmostEqual(fit_result.x[0], 1.00000009)
        self.assertAlmostEqual(fit_result.x[1], 1.)

    def test_parameter_add(self):
        a = Parameter('a')
        b = Parameter('b')
        new = a + b
        self.assertIsInstance(new, sympy.Add)

    def test_symbol_add(self):
        x, y = symbols('x y')
        new = x + y
        self.assertIsInstance(new, sympy.Add)

    def test_symbol_object_add(self):
        from sympy.core.symbol import Symbol
        x = Symbol('x')
        y = Symbol('y')
        new = x + y
        self.assertIsInstance(new, sympy.Add)

if __name__ == '__main__':
    unittest.main()