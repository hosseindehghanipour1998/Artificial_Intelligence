'''
Before Running the code you should install "sympy" by using this command :
    > pip install sympy

In order to use "matplot" to plot the curve :
    > pip install matplotlib
'''



'''
expr = x**3 + 4*x*y - z
expr.subs([(x, 2), (y, 4), (z, 0)])
expr.subs(x,2) 


x = sp.Symbol('x')
x , y = sp.symbols('x y')
'''
#*********************************************************************************
# Libraries
import sympy as sp
from random import random
from Writer import Writer
import matplotlib.pyplot as plt
#*********************************************************************************
# Initializing Symbols
pi = sp.pi 
x , y = sp.symbols('x y')
#*********************************************************************************
# Initial Values Entered By User : (Hard Codded)
f = (sp.sin(10*sp.pi*x)/(2*x)) + (x-1)**4 # change this function based on our own demand.
lowerBoundry = 0.5
upperBoundry = 2.5
steps = 10**-4
plotSteps = 5 * 10**-3
numberOfSamples = 25
g = x**4 + 2*x**5 + 3*x + 2
#*********************************************************************************
# Methods Implementation

def calculateDifferenciation(f,order):
    derivatedFunction = f 
    for i in range(0,order):
        derivatedFunction = sp.diff(derivatedFunction)
        #print("Derivation [" + str(i) + "] : " + str(derivatedFunction))
    return derivatedFunction
###############################################################################
def getRandom( lowerBound , upperBound ):
    value = random()
    scaledValue = lowerBound + (value * (upperBound - lowerBound))
    return scaledValue
###############################################################################
def iterativeHillClimbing(numberOfSamples):
    samples = []
    for i in range (0 , numberOfSamples ):
        value = getRandom(lowerBoundry,upperBoundry)
        localOptimaCoordinates = hillClimbing(f,lowerBoundry,upperBoundry , value , None , False)
        samples.append(localOptimaCoordinates)
        print("Sample No : [" + str(i+1) + "]")
        
    globalOptima = findMinTuple(samples,1)
    print("Gloabl optima : " + str(globalOptima))
    return (globalOptima,samples)
 ###############################################################################       
def findMinTuple( data , keyIndex ):
    return min(data, key = lambda t: t[keyIndex])
###############################################################################
def hillClimbing(expr, lowerBoundry , upperBoundry , randomValue , fileName , writeInFile = True):
    if(writeInFile):
        w = Writer(fileName + ".txt")
        w.clearFile()
    # "expr" is our function
    dx = calculateDifferenciation(expr,1)
    #value = getRandom(lowerBoundry,upperBoundry)
    value_X = randomValue
    slope = 1 if (dx.subs(x,value_X) > 0) else -1  
    amount =  dx.subs(x,value_X)
    derivationAmount = round(float(amount),1)
    while (derivationAmount != 0.0 and value_X >= lowerBoundry and value_X <= upperBoundry ):
        if( slope > 0 ):
            value_X -= steps
        else :
            value_X += steps
        if(writeInFile):
            w.append(str(value_X) + " \t " + str(derivationAmount) )
        amount =  dx.subs(x,value_X)
        derivationAmount = round(float(amount),1)

    print("Done!")
    value_Y = expr.subs(x,value_X)
    
    value_X = round(float(value_X),2)
    value_Y = round(float(value_Y),2)
    return (value_X,value_Y)
###############################################################################
def iterativeHillClimbingPlot(f , lowerBound , upperBound , step , localOptimas , globalOptima ):
    # Draw the function
    x_axis = []
    y_axis = []
    i = lowerBound 
    while(i < upperBound):
        x_axis.append(i)
        y_axis.append(f.subs(x,i))
        i += step
    
    # plotting the function points 
    plt.plot(x_axis, y_axis, label = "function") 
    
    # Plotting Local Optimas
    for item in localOptimas :
        plt.scatter(item[0], item[1], color="black" )
    # Labeling Local Optimas
    plt.scatter(item[0], item[1], color="black" , label = "Local Optimas")
        
    # plottign global Optima
    plt.scatter(globalOptima[0], globalOptima[1], color="red" , label = "Global Optima")
    
    plt.plot([0, globalOptima[0]], [ globalOptima[1],  globalOptima[1]], linestyle="--", color="red")
    plt.plot([globalOptima[0], globalOptima[0]], [ globalOptima[1],0], linestyle="--", color="red")
    plt.annotate(r"$ Global Optima : x = " +str(round(globalOptima[0],2))+ "$", 
             xy=(globalOptima[0],  globalOptima[1]), xytext=(-20, +80), annotation_clip=False, 
             textcoords="offset points", fontsize=16, 
             arrowprops=dict(arrowstyle="<-", connectionstyle="arc3,rad=.5"))
    
    
    # naming the x axis 
    plt.xlabel('x - axis') 
    # naming the y axis 
    plt.ylabel('y - axis') 
    # giving a title to my graph 
    plt.title("IHC : No. of samples : " + str(numberOfSamples) ) 
    plt.legend() 
    
    saveFig(plt , "Plots/IHC_Plot_" , "Plots/figureNumber.txt" )
    
    

   
############################################################################### 
def saveFig(plotPointer , figName , figNumbPath ):
    # Figure Numbering
    filerIO = Writer(figNumbPath)
    lines = filerIO.readFile()
    if ( len(lines) == 0 ):
        filerIO.append(1) 
        lines[0] = 1 
    plotPointer.savefig( str(figName) + str(lines[0]) + '.png')
    filerIO.clearFile()
    filerIO.append(str(int(lines[0]) + 1) )    
###############################################################################
def plot(f,lowerBound,upperBound,target_x,step , plotTitle , arrowLabeling = True):
    # Draw the function
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
    if ( arrowLabeling  ):
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
#*********************************************************************************
def sigmoid(alpha,beta):
    numerated = 1 + sp.exp(alpha/beta) 
    return 1/numerated
#*********************************************************************************
def T(x):
    return 1/x
#*********************************************************************************
def simulatedAnnealing(f,lowerBoundry,upperBoundry):
    simulatedAnnealingIO = Writer("SimulatedAnnealing.txt")
    current = getRandom(lowerBoundry,upperBoundry)
    deltaE = 0
    t = 100000
    while True :
        
        print(t)
        simulatedAnnealingIO.append(t)
        #possibility = sigmoid(deltaE * -1 , t)
        
        nextX = getRandom(lowerBoundry,upperBoundry)
        if ( t <= 0.05 ):
            break
        deltaE = f.subs(x,nextX) - f.subs(x,current)
        possibility = sp.exp(deltaE/t)
        if ( deltaE < 0):
            current = nextX
        else :
            rnd = getRandom(0,1)
            if(rnd > possibility):
                current = nextX
        t *= 0.99
    globalX = current
    globalY = f.subs(x,globalX)
    return (globalX,globalY)        
            
#*********************************************************************************    
##############################################
##################### MAIN ###################
##############################################

######### Hill Climbing #####################
    

#print("Calculating:")   
#value = getRandom(lowerBoundry,upperBoundry)
#localX , localY = hillClimbing(f,lowerBoundry,upperBoundry , value , "HillClimbing" )
#print("("+ str(localX) + "," +  str(localY) + ")")
#plot(f,lowerBoundry,upperBoundry,localX,plotSteps,"Hill Climbing")


######### Iterative Hill Climbing #####################


#
#globalOptima , localOptimas = iterativeHillClimbing(numberOfSamples)
#iterativeHillClimbingPlot(f,lowerBoundry , upperBoundry , plotSteps , localOptimas , globalOptima )
#
#IHC_Locals = Writer("IterativeHillClimbing_LocalOptimas.txt")
#IHC_Locals.arrayToFile(localOptimas)



############# Simulated Annealing ############


print("Simulated Annealing:")  
SA_global = simulatedAnnealing(f,lowerBoundry,upperBoundry)

plot(f,lowerBoundry,upperBoundry,SA_global[0],plotSteps , "Simulated Annealing" , arrowLabeling = False)








