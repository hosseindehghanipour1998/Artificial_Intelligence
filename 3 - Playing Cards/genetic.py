# -*- coding: utf-8 -*-
"""
Created on Tue May 12 02:00:53 2020

@author: Hossein
"""

#============ Imports ====================
import random
import ExternalLibraries.External as ExternalLib
import matplotlib.pyplot as plt
#=========================================


#=====================================================
def deportUnworthyPeople(population):
    if(ExternalLib.ControlRoom.debugMode):
         ExternalLib.FileManager.errors_Writer.append("DEPORT ONWORTHY")
    worthyPop = []
    sum_nums = [] 
    prod_nums = []
    for item in population:
        summ , prod = ExternalLib.caculateFactors(item)
        prod,summ = utility(summ,prod)
        sum_nums.append(summ)
        prod_nums.append(prod)
    
    pop1 = []
    pop2 = []
    for item in population:
        pop1.append(item)
        pop2.append(item)
    ExternalLib.FileManager.sorter_Writer.append("====================== SUM==========================")
    ExternalLib.bubble_sort(sum_nums,pop1)  
    ExternalLib.FileManager.sorter_Writer.append("====================== PROD ==========================")
    ExternalLib.bubble_sort(prod_nums,pop2)
    i = 0 
    while i < ExternalLib.ControlRoom.populationLimit/2 :
        worthyPop.append(pop1[i])
        i += 1
    i = 0 

    for item in pop2 :
        if(len(worthyPop) == ExternalLib.ControlRoom.populationLimit ):
            break
        if ( not item in worthyPop):           
            worthyPop.append(pop2[i])           
    return worthyPop

#================ Extera Functions====================

def isSolution(children):
    if(ExternalLib.ControlRoom.debugMode):
        ExternalLib.FileManager.errors_Writer.append("Is solution")
    child_1_Summation , child_1_Production = ExternalLib.caculateFactors(children[0])
    child_2_Summation , child_2_Production = ExternalLib.caculateFactors(children[1])
    if(   
       ((child_1_Summation == ExternalLib.ControlRoom.goalSummation and child_2_Production == ExternalLib.ControlRoom.goalProduct ) or 
       (child_2_Summation == ExternalLib.ControlRoom.goalSummation and child_1_Production == ExternalLib.ControlRoom.goalProduct )) and ExternalLib.haveIntersection(children) == False ) :
        return True

  

def getBestN(population , exception = False):
    """ Apperoach 2 """  
    minimumSum = 1000
    minimumProd = 1000
    sumChild = None
    prodChild = None
    for child in population : 
        if(ExternalLib.ControlRoom.debugMode):
            ExternalLib.FileManager.errors_Writer.append("GBN - FOR 1")
        summ , prod = ExternalLib.caculateFactors(child)
        util_prod , util_Sum = utility( summ , prod )
        if ( util_prod <= minimumProd) :
            prodChild = child
            minimumProd = util_prod
    for child in population :    
        if(ExternalLib.ControlRoom.debugMode):
            ExternalLib.FileManager.errors_Writer.append("GBS - FOR 2")
        summ , prod = ExternalLib.caculateFactors(child)
        util_prod , util_Sum = utility( summ , prod )
        if ( util_Sum <= minimumSum and (ExternalLib.haveIntersection((prodChild,child)) == False  or exception )):
            minimumSum = util_Sum
            sumChild = child
      
    return (prodChild,sumChild)


  
#================ Main Functions====================
    
def utility(childSum , childProduct ):
    if(ExternalLib.ControlRoom.debugMode):
        ExternalLib.FileManager.errors_Writer.append("UTILITY")
    return (abs(1 -  float(childProduct/ExternalLib.ControlRoom.goalProduct) ), abs(ExternalLib.ControlRoom.goalSummation - childSum) )

def crossOver( father , mother ): 
    if(ExternalLib.ControlRoom.debugMode):
        ExternalLib.FileManager.errors_Writer.append("CROSS OVER")
    child1 = []
    while True :
        if(ExternalLib.ControlRoom.debugMode):
            ExternalLib.FileManager.errors_Writer.append("CROSS OVER - WHILE 1")
        if(len(child1) < ExternalLib.ControlRoom.parentsLength ):
            rnd = random.randint(-4,4)
            if (not mother[rnd]  in child1):
                child1.append(mother[rnd])
        if(len(child1) < ExternalLib.ControlRoom.parentsLength):
            rnd = random.randint(-4,4)
            if (not father[rnd]  in child1):
                child1.append(father[rnd])
        else :
            break
    child2 = []
    for item in range(1,11):
        if(not item in child1):
            child2.append(item)
    probability = random.randint(0,100)
    if(probability > ExternalLib.ControlRoom.mutationProbability):
        child1 , child2 = mutate(child1,child2)        
    return (child1,child2)

def mutate( child , bro):
    while True :
        rnd = random.randint(-4,4)
        if ( (not bro[rnd] in child) and (not child[rnd] in bro) ):
            x = child[rnd]
            child[rnd] = bro[rnd]
            bro[rnd] = x
            return child,bro
#==================================================

def environmet():
    ExternalLib.ControlRoom.generationCounter
    ExternalLib.ControlRoom.population = []
    ExternalLib.FileManager.complete_Writer.clearFile()
    ExternalLib.FileManager.sorter_Writer.clearFile()
    ExternalLib.FileManager.testCase_Writer.clearFile()
    generationCounter = 0
    generationMinitor = 0 
    
    mother , father = ExternalLib.createRandomParents(ExternalLib.ControlRoom.parentsLength)
    
    ExternalLib.FileManager.testCase_Writer.append("Initial Parents : %s | %s" %(mother , father) )
    
    print("=========================================" )
    print("Generation Number : %s" %generationCounter)
    print("=========================================" )
    
    print("initial Parents : %s | %s" %(mother , father) )
    ExternalLib.ControlRoom.restart()
    while True :
        
        # Controling generation
        generationMinitor += 1
        if ( generationMinitor == ExternalLib.ControlRoom.populationLimit ):
            generationMinitor = 0 
            generationCounter += 1
            print("=========================================" )
            print("Generation Number : %s" %generationCounter)
            print("=========================================" )
            
            
        
        #print(ExternalLib.ControlRoom.generationCounter)
        newBornChildren = crossOver(mother,father)
        
        # Writing in File
        ExternalLib.FileManager.complete_Writer.append("===========================")
        ExternalLib.FileManager.complete_Writer.append("Newborn : " + str(newBornChildren))
        
        
        # Creating population
        ExternalLib.ControlRoom.population.append(newBornChildren[0])
        ExternalLib.ControlRoom.population.append(newBornChildren[1])
        #System may halt for  bad test cases. this attributes avoids halting
        haltCounter = 0 
        showException = False
        while True : #Loop 2
            if ( haltCounter >= ExternalLib.ControlRoom.haltsLimit ):
                showException = True
            newParents = getBestN(ExternalLib.ControlRoom.population , exception=showException)
            if ( newParents[0] != None and newParents[1] != None  ):
                mother , father = newParents
                break
            haltCounter += 1
        
        # Writing in File
        ExternalLib.FileManager.complete_Writer.append(ExternalLib.ControlRoom.generationCounter)
        ExternalLib.FileManager.complete_Writer.append("Parents : " + str(newParents))
        ExternalLib.ControlRoom.succeededProdParents.append(newParents[0])
        ExternalLib.ControlRoom.succeededSumParents.append(newParents[1])
        ExternalLib.FileManager.complete_Writer.append(ExternalLib.ControlRoom.population)
        ExternalLib.FileManager.complete_Writer.append(len(ExternalLib.ControlRoom.population))
        
        # Eliminating Unworthy Population
        if ( len(ExternalLib.ControlRoom.population) >= ExternalLib.ControlRoom.populationLimit ):
            ExternalLib.ControlRoom.population = deportUnworthyPeople(ExternalLib.ControlRoom.population)
            
        if( isSolution(newParents) == True ):
            print("Found Solution")
            return newParents,generationCounter
        ExternalLib.ControlRoom.generationCounter += 1

def plotUtilitiesDistinctively():
    curveOneXs = []
    curveOneYs = []
    
    curveTwoXs = []
    curveTwoYs = []
    
    xValue = 0
    for parent in ExternalLib.ControlRoom.succeededProdParents :
        childSum , childProduct = ExternalLib.caculateFactors(parent)
        productU , summationU  = utility(childSum,childProduct)
        
        
        #productU = ( productU + 1 ) * ExternalLib.ControlRoom.goalProduct 
        #products
        curveTwoXs.append(xValue)
        curveTwoYs.append(productU) 
        xValue += 1
    
   
    xValue = 0   
    for parent in ExternalLib.ControlRoom.succeededSumParents :
        childSum , childProduct = ExternalLib.caculateFactors(parent)
        productU , summationU   = utility(childSum,childProduct)
        #Sums
        curveOneXs.append(xValue)
        curveOneYs.append(summationU + ExternalLib.ControlRoom.goalSummation )
        xValue += 1
        
    plt.plot(curveOneXs,curveOneYs , color="blue" , label = "Summation")
    plt.plot(curveTwoXs,curveTwoYs , color="red", label = "Production")
    plt.legend()
    plt.show()
    
def plotUtilitiesOverall(generationsNumber = "Z"):
    curveOneXs = []
    curveOneYs = []
    
    productionUtilies = []
    summationUtilities = []
     
    xValue = 0
    for parent in ExternalLib.ControlRoom.succeededProdParents :
        childSum , childProduct = ExternalLib.caculateFactors(parent)
        productU , summationU  = utility(childSum,childProduct)
        #Prods
        productionUtilies.append(productU)
        
    for parent in ExternalLib.ControlRoom.succeededSumParents :
        childSum , childProduct = ExternalLib.caculateFactors(parent)
        productU , summationU   = utility(childSum,childProduct)
        #Sums
        summationUtilities.append(summationU)
        
    for index in  range(0,len(summationUtilities)):
        curveOneXs.append(xValue)
        xValue += 1
        scaledY = summationUtilities[index] + ExternalLib.scale(productionUtilies[index])
        curveOneYs.append(scaledY)

           
    plt.plot(curveOneXs,curveOneYs , color="blue" , label = "Overal Utility")
    plt.legend() 
    plotTitle = "Plots/Overall_#NoOfGens[" + str(generationsNumber) + "]_"
    ExternalLib.saveFig(plt , plotTitle , "Plots/figureNumber.txt" )
    plt.show()    

def main():
    results = []
    for i in range (0,ExternalLib.ControlRoom.testCaseNo) :           
        print("Calculating...")
        sol,generations = environmet()
        results.append(sol)
        print(str(sol[0]) + "\n" + str(sol[1]))
        print("Done!")
        plotUtilitiesDistinctively()
        plotUtilitiesOverall(generations)
        
        ExternalLib.FileManager.testCase_Writer.append("Number of Generations : %s \n=====================================" %generations )
    print("Totally Done")
    print(len(results))
    for item in results:
        print(item)

        
main()            
        