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
populationSize = 10
iterationNo = 0
#=====================================================
writer1 = Writer("Results/Parents.txt")
write2 = Writer("Results/createBabies.txt")
writer3 = Writer("Results/chooseBEstN.txt")
writer4 = Writer("Results/complete.txt")
writer5 = Writer("Results/sortSome.txt")

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

def haveIntersection(children):
    for item in children[0]:
        if(item in children[1]):
            return True
    return False
def isSolution(children):
    
    child_1_Summation , child_1_Production = caculateFactors(children[0])
    child_2_Summation , child_2_Production = caculateFactors(children[1])
    if(   
       ((child_1_Summation == targetSum and child_2_Production == targetProduct ) or 
       (child_2_Summation == targetSum and child_1_Production == targetProduct )) and haveIntersection(children) == False ) :
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
        util_prod , util_Sum = utility( summ , prod )
        if ( util_Sum <= minimumSum ):
            minimumSum = util_Sum
            sumChild = child
    
    
    for child in population :
        summ , prod = caculateFactors(child)
        util_prod , util_Sum = utility( summ , prod )
        if ( util_prod <= minimumProd and sameTwoChildren(child , sumChild ) == False) :
            prodChild = child
            minimumProd = util_prod

            
    writer3.append("{%s : sum = %s }  | { %s : mult = %s } |It : %s | " %(sumChild,minimumSum , prodChild ,minimumProd , iterationNo ))
    return sumChild , prodChild      

def bubble_sort(nums,pop):
    # We set swapped to True so the loop looks runs at least once
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
    writer5.append("================================================")           
    writer5.append("IT : %s"%iterationNo)            
    writer5.append(nums)
    
def deportUnworthyPeople(population):
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
    
    bubble_sort(sum_nums,pop1)    
    bubble_sort(prod_nums,pop2)
    i = 0 
    while i < populationSize/2 :
        worthyPop.append(pop1[i])
        i += 1
    i = 0 
    while (len(worthyPop) < populationSize ):
        if ( not pop2[i] in worthyPop):
            worthyPop.append(pop2[i])
        i += 1
    return worthyPop

def countOverlap(li1 , li2):
    overlap = 0 
    for item in li1 :
        if(item in li2):
            overlap += 1
    return overlap    
#================ Main Functions====================
    
def utility(childSum , childProduct ):
    return (abs(1 -  float(childProduct/targetProduct) ), abs(targetSum - childSum) )

def crossOver( father , mother ):  
#    from random import shuffle
#    shuffle(mother)
#    shuffle(father)
    # approach 1
#    children = []
#    child = []
#    write2.append("Mother : " + str(father) +  " Father : " + str(mother))
#    i = 0 
#    allowed = True
#    while i < 2 : 
#        child = []
#        while(True):
#            
#            if(len(child) < parentsLength ):
#                rndIndex = random.randint(-4,4)
#                g1 = father[rndIndex]
#                if(not g1 in child):
#                    child.append(g1)
#            
#            if(len(child) < parentsLength ):
#                rndIndex = random.randint(-4,4)
#                g2 = mother[rndIndex]
#                if(not g2 in child):
#                    child.append(g2)
#            else :
#                break
#        
#        probability = random.randint(0,100)
#        if(probability > mutationProbability):
#            if ( len ( children ) == 1 ):
#                child = mutate2( child , children[0] )
#            else :
#                child = mutate(child)        
#        if ( len(children) > 0 ):
#            if(sameTwoChildren(child,children[0]) == True ):
#                write2.append("Same Child Born")
#                i -= 1
#                allowed = False
#            else :
#                allowed = True
#        if ( allowed ): 
#            children.append(child)
#            write2.append(child)            
#        i += 1
    child1 = []
    while(True):

        if(len(child1) < parentsLength ):
            rndIndex = random.randint(-4,4)
            g1 = father[rndIndex]
            if(not g1 in child1):
                child1.append(g1)
        
        if(len(child1) < parentsLength ):
            rndIndex = random.randint(-4,4)
            g2 = mother[rndIndex]
            if(not g2 in child1):
                child1.append(g2)
        else :
            break

    child2 = []
    for item in range(1,11):
        if(not item in child1):
            child2.append(item)
    children = [child1,child2]
    
    return children

def mutate( child ):    
    while True :
        rndNumber = random.randint(1,10)
        rndIndex = random.randint(0,4)
        if ( (not rndNumber in child) ):
            child[rndIndex] = rndNumber
            return child

def mutate2( child , brother ):    
    while True :
        rndNumber = random.randint(1,10)
        rndIndex = random.randint(0,4)
        if ( (not rndNumber in child) and (not rndNumber in brother) ):
            child[rndIndex] = rndNumber
            return child

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
        
        print(iterationNo)
        newBornChildren = crossOver(mother,father)
        writer4.append("===========================")
        writer4.append("Newborn : %s" %newBornChildren)
        population.append(newBornChildren[0])
        population.append(newBornChildren[1])
        newParents = getBestN(population)
        mother , father = newParents
        
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
    print("Calculating...")
    m , f = environmet()
    print(str(m) + "\n" + str(f))
    print("Done!")
        
main()            
        