# -*- coding: utf-8 -*-
"""
Created on Tue May 12 02:00:53 2020

@author: Hossein
"""

#============ Imports ====================
from random import random

#=========================================
targetProduct = 360
targetSum = 36
parentsLength = 5 
#================ Extera Functions====================
def getRandom( lowerBound , upperBound ):
    #returns a random number between the wanted boundries
    value = random()
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
    
    for i in range( parentsLength - 1 ):
        rnd = getRandom(1,10)
        mother.append(rnd)
    for i in range ( parentsLength * 2 ):
        if ( not i in mother ):
            father.append(i)
    print("Mother : " +  str(mother))
    print("Father : " +  str(father))
    return (mother,father)    

def getBestN(allChildren):
    minimumSum = targetSum
    minimumProd = targetProduct
    sumChild = None
    prodChild = None
    
    for child in allChildren :
        summ , prod = caculateFactors(child)
        util_Sum , util_prod = utility( summ , prod )
        if ( util_Sum < minimumSum ):
            sumChild = child
   
    for child in allChildren :
        summ , prod = caculateFactors(child)
        util_Sum , util_prod = utility( summ , prod )
        if ( prodChild < minimumProd and sameTwoChildren(child , sumChild ) == False) :
            prodChild = child
        
    return sumChild , prodChild      
        
       
#================ Main Functions====================
    
def utility(childSum , childProduct ):
    return (targetProduct/childProduct , targetSum - childSum)

def crossOver( father , mother ):
    # 6 types of crossing over :
    children = []
    children.append( father[0:3] + mother[3:5] )
    children.append( father[3:5] + mother[0:3] )
    children.append( father[2:5] + mother[0:2] )
    children.append( father[0:2] + mother[2:5] )
    children.append( father[3:5] + mother[0:3] )
    children.append( father[0:3] + mother[3:5] )
    return children

def mutate(child):    
    while True :
        rndNumber = getRandom(1,10)
        rndIndex = getRandom(0,4)
        if ( not rndNumber in child ):
            child[rndIndex] = rndNumber
            break


def environmet():
    parents = createRandomParents(parentsLength)
    mother = parents[0]
    father = parents[1]
    while True :
        newBornChildren = crossOver(mother,father)
        mother , father = getBestN(newBornChildren)
        newParents = (mother , father)
        if( isSolution(newParents) == True ):
            print("Found Solution")
            return newParents
        print("Not Good Enough")

def main():
    print("Calculating...")
    m , f = environmet()
    print(str(m) + "\n" + str(f))
        
main()            
        