'''
Before Running the code you should install "sympy" by using this command :
    > pip install sympy

I order to use "matplot" to plot the curve :
    > pip install matplotlib
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
from Writer import Writer
import matplotlib.pyplot as plt
############################
# Initializing Symbols
pi = sp.pi 
x , y = sp.symbols('x y')
#############################################
# Initial Values Entered By User : (Hard Codded)
f = (sp.sin(10*sp.pi*x)/(2*x)) + (x-1)**4 # change this function based on our own demand.
lowerBoundry = 0.5
upperBoundry = 2.5
steps = 10**-4
plotSteps = 5 * 10**-3
g = x**4 + 2*x**5 + 3*x + 2
#############################################
# Methods Implementation

def calculateDifferenciation(f,order):
    derivatedFunction = f 
    for i in range(0,order):
        derivatedFunction = sp.diff(derivatedFunction)
        #print("Derivation [" + str(i) + "] : " + str(derivatedFunction))
    return derivatedFunction

def getRandom( lowerBound , upperBound ):
    value = random()
    scaledValue = lowerBound + (value * (upperBound - lowerBound))
    return scaledValue

def iterativeHillClimbing():
    

def hillClimbing(expr, lowerBoundry , upperBoundry , randomValue):
    w = Writer("results.txt")
    w.clearFile()
    # "expr" is our function
    dx = calculateDifferenciation(expr,1)
    #value = getRandom(lowerBoundry,upperBoundry)
    value = randomValue
    slope = 1 if (dx.subs(x,value) > 0) else -1  
    amount =  dx.subs(x,value)
    derivationAmount = round(float(amount),1)
    while (derivationAmount != 0.0 and value >= lowerBoundry and value <= upperBoundry ):
        if( slope > 0 ):
            value -= steps
        else :
            value += steps

        w.append(str(value) + " \t " + str(derivationAmount) )
        amount =  dx.subs(x,value)
        derivationAmount = round(float(amount),1)

    print("Done!")
    return value

def plot(f,lowerBound,upperBound,target_x,step , plotTitle):
    x_axis = []
    y_axis = []
    i = lowerBound 
    while(i < upperBound):
        x_axis.append(i)
        y_axis.append(f.subs(x,i))
        i += step
    target_y = f.subs(x,target_x)
   
    # plotting the function points 
    plt.plot(x_axis, y_axis, label = "function")   
    # plotting the taget(local optima) points 
    #plt.plot(target_x, target_y, label = "Local Minima") 
    plt.scatter(target_x, target_y, color="black")
    plt.plot([0, target_x], [target_y, target_y], linestyle="--", color="black")
    plt.plot([target_x, target_x], [target_y,0], linestyle="--", color="black")
    plt.annotate(r"$ x = " + str(round(target_x,2)) + "$", 
             xy=(target_x, target_y), xytext=(-20, +80), annotation_clip=False, 
             textcoords="offset points", fontsize=16, 
             arrowprops=dict(arrowstyle="<-", connectionstyle="arc3,rad=.5"))
    # naming the x axis 
    plt.xlabel('x - axis') 
    # naming the y axis 
    plt.ylabel('y - axis') 
    # giving a title to my graph 
    plt.title(plotTitle) 
    # show a legend on the plot 
    plt.legend()     
    # function to show the plot 
    plt.show() 
    
##############################################
    
print("Calculating:")   
value = getRandom(lowerBoundry,upperBoundry)
localX = localOptima = hillClimbing(f,lowerBoundry,upperBoundry , value )
print(localX)
plot(f,lowerBoundry,upperBoundry,localX,plotSteps,"Hill Climbing')
