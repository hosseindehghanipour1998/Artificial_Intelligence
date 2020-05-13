# -*- coding: utf-8 -*-
"""
Created on Tue May 12 02:00:53 2020

@author: Hossein
"""

#============ Imports ====================
import random
from math import *
from ExternalLibraries.Writer import Writer as Writer
from ExternalLibraries.External import External as ExternalLib

#=========================================

class ControlRoom:
    #Static Arrtibutes
    goalProduct = 360
    goalSummation = 36
    parentsLength = 5 
    mutationProbability = 40
    populationLimit = 50
    generationCounter = 0
    haltsLimit = 30
    debugMode = False
    testCaseNo = 1
#=====================================================
class FileManager :
    complete_Writer = Writer("Results/complete.txt")
    sorter_Writer = Writer("Results/sorter.txt")
    errors_Writer = Writer("Results/Errors.txt")

#================ Extera Functions====================

def isSolution(children):
    if(ControlRoom.debugMode):
        FileManager.errors_Writer.append("Is solution")
    child_1_Summation , child_1_Production = ExternalLib.caculateFactors(children[0])
    child_2_Summation , child_2_Production = ExternalLib.caculateFactors(children[1])
    if(   
       ((child_1_Summation == ControlRoom.goalSummation and child_2_Production == ControlRoom.goalProduct ) or 
       (child_2_Summation == ControlRoom.goalSummation and child_1_Production == ControlRoom.goalProduct )) and ExternalLib.haveIntersection(children) == False ) :
        return True

  

def getBestN(population , exception = False):
    """ Apperoach 2 """  
    minimumSum = 1000
    minimumProd = 1000
    sumChild = None
    prodChild = None
    for child in population : 
        if(ControlRoom.debugMode):
            FileManager.errors_Writer.append("GBN - FOR 1")
        summ , prod = ExternalLib.caculateFactors(child)
        util_prod , util_Sum = utility( summ , prod )
        if ( util_prod <= minimumProd) :
            prodChild = child
            minimumProd = util_prod
    for child in population :    
        if(ControlRoom.debugMode):
            FileManager.errors_Writer.append("GBS - FOR 2")
        summ , prod = ExternalLib.caculateFactors(child)
        util_prod , util_Sum = utility( summ , prod )
        if ( util_Sum <= minimumSum and (ExternalLib.haveIntersection((prodChild,child)) == False  or exception )):
            minimumSum = util_Sum
            sumChild = child
      
    return (prodChild,sumChild)


  
#================ Main Functions====================
    
def utility(childSum , childProduct ):
    if(ControlRoom.debugMode):
        FileManager.errors_Writer.append("UTILITY")
    return (abs(1 -  float(childProduct/ControlRoom.goalProduct) ), abs(ControlRoom.goalSummation - childSum) )

def crossOver( father , mother ): 
    if(ControlRoom.debugMode):
        FileManager.errors_Writer.append("CROSS OVER")
    child1 = []
    while True :
        if(ControlRoom.debugMode):
            FileManager.errors_Writer.append("CROSS OVER - WHILE 1")
        if(len(child1) < ControlRoom.parentsLength ):
            rnd = random.randint(-4,4)
            if (not mother[rnd]  in child1):
                child1.append(mother[rnd])
        if(len(child1) < ControlRoom.parentsLength):
            rnd = random.randint(-4,4)
            if (not father[rnd]  in child1):
                child1.append(father[rnd])
        else :
            break
    child2 = []
    for item in range(1,11):
        if(not item in child1):
            child2.append(item)
    prob = random.randint(0,100)
    if(prob > ControlRoom.mutationProbability):
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
    ControlRoom.generationCounter
    FileManager.complete_Writer.clearFile()
    FileManager.sorter_Writer.clearFile()
    population = []
    
    

    
    parents = ExternalLib.createRandomParents(ControlRoom.parentsLength)
    
    mother = parents[0]
    father = parents[1]
    
    population.append(mother)
    population.append(father)


    while True :
        print(ControlRoom.generationCounter)
        newBornChildren = crossOver(mother,father)
        FileManager.complete_Writer.append("===========================")
        FileManager.complete_Writer.append("Newborn : " + str(newBornChildren))
        if ( newBornChildren[0] != None ):
            population.append(newBornChildren[0])
        if ( newBornChildren[1] != None ):
            population.append(newBornChildren[1])
        haltCounter = 0 
        showException = False
        while True : #Loop 2
            if ( haltCounter >= ControlRoom.haltsLimit ):
                showException = True
            newParents = getBestN(population , exception=showException)
            if ( newParents[0] != None and newParents[1] != None  ):
                mother , father = newParents
                break
            haltCounter += 1
        FileManager.complete_Writer.append(ControlRoom.generationCounter)
        FileManager.complete_Writer.append("Parents : " + str(newParents))
        FileManager.complete_Writer.append(population)
        FileManager.complete_Writer.append(len(population))
        
        
        if ( len(population) >= ControlRoom.populationLimit ):
            population = ExternalLib.deportUnworthyPeople(population)
            
        if( isSolution(newParents) == True ):
            print("Found Solution")
            return newParents
        ControlRoom.generationCounter += 1


        

def main():
    results = []
    for i in range (0,ControlRoom.testCaseNo) :           
        print("Calculating...")
        sol = environmet()
        results.append(sol)
        print(str(sol[0]) + "\n" + str(sol[1]))
        print("Done!")
    print("Totally Done")
    print(len(results))
    for item in results:
        print(item)
        
main()            
        