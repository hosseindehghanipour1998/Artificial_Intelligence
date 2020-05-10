'''
Before Running the code you should install "sympy" by using this command :
    > pip install sympy

In order to use "matplot" to plot the curve :
    > pip install matplotlib

Attentions :  In order to see the plots , go to the "plots" foder in this project.
'''

#*********************************************************************************
# Libraries
import sympy as sp
from random import random
import matplotlib.pyplot as plt
from ExtraLibraries.Writer import Writer as Writer
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
numberOfSamples = int(sp.Abs(upperBoundry - lowerBoundry) * 20)
g = x**4 + 2*x**5 + 3*x + 2
h = (sp.sin(2*x)/x) * (sp.cos(x**(sp.exp(1))) * sp.pi * sp.ln(2*x))
#*********************************************************************************
#*********************** Methods Implementation **********************************
#*********************************************************************************
def calculateDifferenciation(f,order):
    derivatedFunction = f 
    for i in range(0,order):
        derivatedFunction = sp.diff(derivatedFunction)
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
        localOptimaCoordinates = hillClimbing(f,lowerBoundry,upperBoundry , value , None)
        samples.append(localOptimaCoordinates)
        print("Sample No : [" + str(i+1) + "]")
        
    globalOptima = findMinTuple(samples,1)
    print("Gloabl optima : " + str(globalOptima))
    return (globalOptima,samples)
###############################################################################       
def findMinTuple( data , keyIndex ):
    return min(data, key = lambda t: t[keyIndex])
###############################################################################
def hillClimbing(expr, lowerBoundry , upperBoundry , randomValue , fileName):
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
        amount =  dx.subs(x,value_X)
        derivationAmount = round(float(amount),1)
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
    
    
    plt.xlabel('x - axis') 
    plt.ylabel('y - axis') 
    plt.title("IHC : No. of samples : " + str(numberOfSamples) ) 
    plt.legend()    
    saveFig(plt , "Plots/IHC_Plot_" , "Plots/figureNumber.txt" )
    plt.show()
       
############################################################################### 
def saveFig(plotPointer , figName , figNumbPath ):
    filerIO = Writer(figNumbPath)
    lines = filerIO.readFile()
    if ( len(lines) == 0 ):
        filerIO.append(1) 
        lines[0] = 1 
    plotPointer.savefig( str(figName) + str(lines[0]) + '.png')
    filerIO.clearFile()
    filerIO.append(str(int(lines[0]) + 1) )    
###############################################################################
def plot(f,lowerBound,upperBound,target_x,step , plotTitle , arrowLabeling = True , arrowLabelingTitle = "x = " , scatterColor = "black" , scatterLabel = "Minima"):
    x_axis = []
    y_axis = []
    i = lowerBound 
    while(i < upperBound):
        x_axis.append(i)
        y_axis.append(f.subs(x,i))
        i += step
    target_y = f.subs(x,target_x)
    plt.plot(x_axis, y_axis, label = "function")   
    plt.scatter(target_x, target_y,label = scatterLabel , color="black")
    if ( arrowLabeling  ):
        plt.plot([0, target_x], [target_y, target_y], linestyle="--", color=scatterColor)
        plt.plot([target_x, target_x], [target_y,0], linestyle="--", color=scatterColor)
        plt.annotate(r"$ " + str(arrowLabelingTitle) + "  " + str(round(target_x,2)) + "$", 
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
    saveFig(plt,"Plots/" + str(plotTitle),"Plots/figureNumber.txt")
    plt.show()

#*********************************************************************************
def simulatedAnnealing(f,lowerBoundry,upperBoundry):
    current = getRandom(lowerBoundry,upperBoundry)
    deltaE = 0
    tMax = 10**5
    tMin = 0.05
    steps = 0.99
    t = tMax
    while True :
        nextX = getRandom(lowerBoundry,upperBoundry)
        if ( t <= tMin ):
            break
        deltaE = f.subs(x,nextX) - f.subs(x,current)
        possibility = sp.exp(deltaE/t)
        if ( deltaE < 0):
            current = nextX
        else :
            rnd = getRandom(0,1)
            if(rnd > possibility):
                current = nextX
        t *= steps
    globalX = current
    globalY = f.subs(x,globalX)
    return (globalX,globalY)        
            
###################################################### MAIN #########################################
    

## Hill Climbing ##
print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print("Calculating Hillclimbing")   
value = getRandom(lowerBoundry,upperBoundry)
HC_localX , HC_localY = hillClimbing(f,lowerBoundry,upperBoundry , value , "HillClimbing" )
print("Local Minima : ("+ str(HC_localX) + "," +  str(HC_localY) + ")")
plot(f,lowerBoundry,upperBoundry,HC_localX,plotSteps,"Hill Climbing")


## Iterated Hill Climbing ##
print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print("Calculating Iterative Hill Climbing : ") 
print("Number of Samples : " + str(numberOfSamples))
IHC_GlobalOptima , IHC_LocalOptimas = iterativeHillClimbing(numberOfSamples)
iterativeHillClimbingPlot(f,lowerBoundry , upperBoundry , plotSteps , IHC_LocalOptimas , IHC_GlobalOptima )



## Simulated Annealing ##

# Testing : f(x) 
print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(" Simulated Annealing: \n Please Wait for 20 seconds ")  
print("Processing ... " ) 
SA_global_1 = simulatedAnnealing(f,lowerBoundry,upperBoundry)
plot(f,lowerBoundry,upperBoundry,SA_global_1[0],plotSteps , "Simulated Annealing" , arrowLabeling = True,scatterColor="red", scatterLabel = "Global Minima")

# Testing : h(x) 
print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(" Simulated Annealing: \n Please Wait for 20 seconds ") 
print("Processing ... " ) 
SA_global_2 = simulatedAnnealing(h,0.5,5.4)
plot(h,0.5,5.4,SA_global_2[0],plotSteps , "Simulated Annealing" , arrowLabeling = True , scatterColor="red" , scatterLabel = "Global Minima")
################################################### End Of MAIN #########################################



