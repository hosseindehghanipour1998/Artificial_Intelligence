# -*- coding: utf-8 -*-
"""
Created on Tue May 12 02:00:53 2020

@author: Hossein
"""

#============ Imports ====================
import random
from math import *
from ExternalLibraries.Writer import Writer as Writer
#=========================================
targetProduct = 360
targetSum = 36
parentsLength = 5 

#=====================================================
writer1 = Writer("Results/Parents.txt")
write2 = Writer("Results/createBabies.txt")
writer3 = Writer("Results/chooseBEstN.txt")

writer1.clearFile();
write2.clearFile()
writer3.clearFile()
#================ Extera Functions====================
def getRandom( lowerBound , upperBound ):
    #returns a random number between the wanted boundries
    value = random.random()
    scaledValue = lowerBound + (value * (upperBound - lowerBound))
    return scaledValue

def sameTwoChildren(childOne , childTwo):
    appearance = 0 
    for item in childOne :
        if ( not item in childTwo ):
            return False
        appearance += 1
    if ( appearance == len(childOne)):
        return True
    return False
        
def caculateFactors(child):
    summation = 0 
    production = 1  
#    print("Len : " + str((child)))
    for chromosome in child:
        summation += chromosome
        production *= chromosome
    return summation,production

def isSolution(children):
    
    child_1_Summation , child_1_Production = caculateFactors(children[0])
    child_2_Summation , child_2_Production = caculateFactors(children[1])
    if(   
       (child_1_Summation == targetSum and child_2_Production == targetProduct ) or 
       (child_2_Summation == targetSum and child_1_Production == targetProduct ) ) :
        return True

def createRandomParents(parentsLength):
    mother = []
    father = []
    i = 0 
    while (len(mother) != parentsLength):
        i += 1
        rnd = int(getRandom(1,10))
        if(not rnd in mother):
            mother.append(rnd)
            
    for i in range (1,11):
        if ( not i in mother ):
            father.append(i)
            
#    print("Mother : " +  str(mother))
#    print("Father : " +  str(father))
    return (mother,father)    

def getBestN(population):

    #writer.clearFile()
    minimumSum = targetSum
    minimumProd = 1000
    sumChild = None
    prodChild = None
    
    
    for child in population :       
        summ , prod = caculateFactors(child)
        util_Sum , util_prod = utility( summ , prod )
        if ( util_Sum <= minimumSum ):
            minimumSum = util_Sum
            sumChild = child
    
    
    for child in population :
        summ , prod = caculateFactors(child)
        util_Sum , util_prod = utility( summ , prod )
        writer3.append(str(child) + "  \  " + str(util_prod))
        if ( util_prod <= minimumProd and sameTwoChildren(child , sumChild ) == False) :
            prodChild = child
            minimumProd = util_prod     
    return sumChild , prodChild      
       
#================ Main Functions====================
    
def utility(childSum , childProduct ):
    return ( float(childProduct/targetProduct) , abs(targetSum - childSum) )

def crossOver( father , mother ):   

    children = []
    child = []
    write2.append("Mother : " + str(father) +  " Father : " + str(mother))
    i = 0 
    allowed = True
    while i < 2 : 
        child = []
        while(True):
            
            if(len(child) < parentsLength ):
                rndIndex = random.randint(-4,4)
                g1 = father[rndIndex]
                if(not g1 in child):
                    child.append(g1)
            
            if(len(child) < parentsLength ):
                rndIndex = random.randint(-4,4)
                g2 = mother[rndIndex]
                if(not g2 in child):
                    child.append(g2)
            else :
                break
            
        if ( len(children) > 0 ):
            if(sameTwoChildren(child,children[0]) == False ):
                write2.append("Same Child Born")
                i -= 1
                allowed = False
            else :
                allowed = True
        if ( allowed ):        
            children.append(child)
            write2.append(child)            
        i += 1
    return children

def mutate(child):    
    while True :
        rndNumber = getRandom(1,10)
        rndIndex = getRandom(0,4)
        if ( not rndNumber in child ):
            child[rndIndex] = rndNumber
            break
#==================================================

def environmet():
    population = []
    iterationNo = 0
    
    parents = createRandomParents(parentsLength)
    
    mother = parents[0]
    father = parents[1]
    
    population.append(mother)
    population.append(father)
    writer1.append(parents)
    
    while True :
        
        print(iterationNo)
        newBornChildren = crossOver(mother,father)
        population.append(newBornChildren[0])
        population.append(newBornChildren[1])
        newParents = getBestN(population)
        mother , father = newParents
        population = [ mother , father]
        writer1.append(newParents)
        if( isSolution(newParents) == True ):
            print("Found Solution")
            return newParents
        iterationNo += 1

        

def main():
    print("Calculating...")
    m , f = environmet()
    print(str(m) + "\n" + str(f))
    print("Done!")
        
main()            
        