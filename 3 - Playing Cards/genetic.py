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
mutationProbability = 40
populationSize = 50
iterationNo = 0
numberOfHalts = 30
debuMode = False
testCaseNo = 1
globalX = 0 
#=====================================================
writer1 = Writer("Results/Parents.txt")
write2 = Writer("Results/createBabies.txt")
writer3 = Writer("Results/chooseBEstN.txt")
writer4 = Writer("Results/complete.txt")
writer5 = Writer("Results/sortSome.txt")
writer6 = Writer("Results/population.txt")
writer7 = Writer("Results/Errors.txt")

#================ Extera Functions====================
def getRandom( lowerBound , upperBound ):
    #returns a random number between the wanted boundries
    value = random.random()
    scaledValue = lowerBound + (value * (upperBound - lowerBound))
    return scaledValue

def sameTwoChildren(childOne , childTwo):
    if(debuMode):
        writer7.append("Same Two Children")
    appearance = 0 
    for item in childOne :
        if ( not item in childTwo ):
            return False
        appearance += 1
    if ( appearance == len(childOne)):
        return True
    return False
        
def caculateFactors(child):
    if(debuMode):
        writer7.append("Calculate Factor")
    summation = 0 
    production = 1  
#    print("Len : " + str((child)))
    for chromosome in child:
        summation += chromosome
        production *= chromosome
    return summation,production

def haveIntersection(children):
    if(debuMode):
        writer7.append("Hvae Intersection")
    for item in children[0]:
        if(item in children[1]):
            return True
    return False
def isSolution(children):
    if(debuMode):
        writer7.append("Is solution")
    child_1_Summation , child_1_Production = caculateFactors(children[0])
    child_2_Summation , child_2_Production = caculateFactors(children[1])
    if(   
       ((child_1_Summation == targetSum and child_2_Production == targetProduct ) or 
       (child_2_Summation == targetSum and child_1_Production == targetProduct )) and haveIntersection(children) == False ) :
        return True

def createRandomParents(parentsLength):
    if(debuMode):
        writer7.append("Create Random Parents")
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

    return (mother,father)    

def getBestN(population , exception = False):
    global globalX
    """ Apperoach 2 """  
    minimumSum = 1000
    minimumProd = 1000
    sumChild = None
    prodChild = None
    for child in population : 
        if(debuMode):
            writer7.append("GBN - FOR 1")
        summ , prod = caculateFactors(child)
        util_prod , util_Sum = utility( summ , prod )
        if ( util_prod <= minimumProd) :
            prodChild = child
            minimumProd = util_prod
    for child in population :    
        if(debuMode):
            writer7.append("GBS - FOR 2")
        summ , prod = caculateFactors(child)
        util_prod , util_Sum = utility( summ , prod )
        if ( util_Sum <= minimumSum and (haveIntersection((prodChild,child)) == False  or exception )):
            minimumSum = util_Sum
            sumChild = child
      
    return (prodChild,sumChild)

def findIntersection(c1,c2):
    if(debuMode):
        writer7.append("FIND INTERSECTION")
    for i in c1 :
        if(i in c2):
            return c2.index(i)
    return -1
def bubble_sort(nums,pop):
    if(debuMode):
        writer7.append("BUBBLE SORT")
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(nums) - 1):
            if nums[i] > nums[i + 1]:
                # Swap the elements
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
                pop[i], pop[i + 1] = pop[i + 1], pop[i]
                # Set the flag to True so we'll loop again
                swapped = True
               
    writer5.append("IT : \n %s" % (iterationNo) )           
    writer5.append(nums)
    writer5.append(pop)

    
    
def deportUnworthyPeople(population):
    if(debuMode):
        writer7.append("DEPORT ONWORTHY")
    worthyPop = []
    sum_nums = [] 
    prod_nums = []
    for item in population:
        summ , prod = caculateFactors(item)
        prod,summ   = utility(summ,prod)
        sum_nums.append(summ)
        prod_nums.append(prod)
    
    pop1 = []
    pop2 = []
    for item in population:
        pop1.append(item)
        pop2.append(item)
    writer5.append("====================== SUM==========================")
    bubble_sort(sum_nums,pop1)  
    writer5.append("====================== PROD ==========================")
    bubble_sort(prod_nums,pop2)
    i = 0 
    while i < populationSize/2 :
        worthyPop.append(pop1[i])
        i += 1
    i = 0 

    for item in pop2 :
        if(len(worthyPop) == populationSize ):
            break
        if ( not item in worthyPop):           
            worthyPop.append(pop2[i])
            
    return worthyPop

def countOverlap(li1 , li2):
    if(debuMode):
        writer7.append("COUNT OVERLAP")
    overlap = 0 
    for item in li1 :
        if(item in li2):
            overlap += 1
    return overlap    
#================ Main Functions====================
    
def utility(childSum , childProduct ):
    if(debuMode):
        writer7.append("UTILITY")
    return (abs(1 -  float(childProduct/targetProduct) ), abs(targetSum - childSum) )

def crossOver( father , mother ): 
    if(debuMode):
        writer7.append("CROSS OVER")
    child1 = []
    while True :
        if(debuMode):
            writer7.append("CROSS OVER - WHILE 1")
        if(len(child1) < parentsLength ):
            rnd = random.randint(-4,4)
            if (not mother[rnd]  in child1):
                child1.append(mother[rnd])
        if(len(child1) < parentsLength):
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
    if(prob > mutationProbability):
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
    global  iterationNo
    writer1.clearFile()
    write2.clearFile()
    writer3.clearFile()
    writer4.clearFile()
    writer5.clearFile()
    population = []
    
    

    
    parents = createRandomParents(parentsLength)
    
    mother = parents[0]
    father = parents[1]
    
    population.append(mother)
    population.append(father)
    writer1.append(parents)

    while True :
        writer6.append("============================")
        print(iterationNo)
        newBornChildren = crossOver(mother,father)
        writer4.append("===========================")
        writer4.append("Newborn : " + str(newBornChildren))
        if ( newBornChildren[0] != None ):
            population.append(newBornChildren[0])
        if ( newBornChildren[1] != None ):
            population.append(newBornChildren[1])
        haltCounter = 0 
        showException = False
        while True : #Loop 2
            if ( haltCounter >= numberOfHalts ):
                showException = True
            newParents = getBestN(population , exception=showException)
            if ( newParents[0] != None and newParents[1] != None  ):
                mother , father = newParents
                break
            haltCounter += 1
        writer4.append(iterationNo)
        writer4.append("Parents : " + str(newParents))
        writer4.append(population)
        writer4.append(len(population))
        
        
        if ( len(population) >= populationSize ):
            population = deportUnworthyPeople(population)
            
            
        writer1.append(newParents)
        if( isSolution(newParents) == True ):
            print("Found Solution")
            return newParents
        iterationNo += 1


        

def main():
    results = []
    for i in range (0,testCaseNo) :           
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
        