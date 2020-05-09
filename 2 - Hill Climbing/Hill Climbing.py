'''
Before Running the code you should install "sympy" by using this command :
    > pip install sympy
'''


'''
expr = x**3 + 4*x*y - z
expr.subs([(x, 2), (y, 4), (z, 0)])
 

'''

import sympy as sp

pi = sp.pi 
# x = sp.Symbol('x')
x , y = sp.symbols('x y')

f = (sp.sin(10*sp.pi*x)/(2*x)) + (x-1)**4 # change this function based on our own demand.
g = x**4 + 2*x**5 + 3*x + 2


def calculateDifferenciation(f,order):
    derivatedFunction = f 
    for i in range(0,order):
        derivatedFunction = sp.diff(derivatedFunction)
        print("Derivation [" + str(i) + "] : " + str(derivatedFunction))
    return derivatedFunction


calculateDifferenciation(g,2)


