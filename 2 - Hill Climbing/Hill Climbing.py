'''
Before Running the code you should install "sympy" by using this command :
    > pip install sympy
'''


'''
expr = x**3 + 4*x*y - z
expr.subs([(x, 2), (y, 4), (z, 0)])
expr.subs(x,2) 


x = sp.Symbol('x')
x , y = sp.symbols('x y')
'''
############################
# Libraries
import sympy as sp
from random import random
############################
# Initializing Symbols
pi = sp.pi 
x , y = sp.symbols('x y')
#############################################
# Initial Values Entered By User : (Hard Codded)
f = (sp.sin(10*sp.pi*x)/(2*x)) + (x-1)**4 # change this function based on our own demand.
lowerBoundry = 0.5
upperBoundry = 2.5
g = x**4 + 2*x**5 + 3*x + 2
#############################################


def calculateDifferenciation(f,order):
    derivatedFunction = f 
    for i in range(0,order):
        derivatedFunction = sp.diff(derivatedFunction)
        print("Derivation [" + str(i) + "] : " + str(derivatedFunction))
    return derivatedFunction

def getRandom( lowerBound , upperBound ):
    value = random()
    scaledValue = lowerBound + (value * (upperBound - lowerBound))
    return scaledValue

#calculateDifferenciation(g,2)
#print(g.subs(x,3))

def hillClimbing(expr, lowerBoundry , upperBoundry):
    # "expr" is our function
    difference = calculateDifferenciation(expr,1)
    value = random()
    print(value)
    
hillClimbing(f,lowerBoundry,upperBoundry)
