import random
import genetic
from genetic import ControlRoom as CR
from genetic import FileManager as FM
def bubble_sort(nums,pop):
    if(CR.debugMode):
        FM.errors_Writer.append("BUBBLE SORT")
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
               
    FM.sorter_Writer.append("IT : \n %s" % (CR.generationCounter) )           
    FM.sorter_Writer.append(nums)
    FM.sorter_Writer.append(pop)



def findIntersection(c1,c2):
    if(CR.debugMode):
        FM.errors_Writer.append("FIND INTERSECTION")
    for i in c1 :
        if(i in c2):
            return c2.index(i)
    return -1


def haveIntersection(children):
    if(CR.debugMode):
        FM.errors_Writer.append("Hvae Intersection")
    for item in children[0]:
        if(item in children[1]):
            return True
    return False



def sameTwoChildren(childOne , childTwo):
    if(CR.debugMode):
        FM.errors_Writer.append("Same Two Children")
    appearance = 0 
    for item in childOne :
        if ( not item in childTwo ):
            return False
        appearance += 1
    if ( appearance == len(childOne)):
        return True
    return False



    
def deportUnworthyPeople(population):
    if(CR.debugMode):
        FM.errors_Writer.append("DEPORT ONWORTHY")
    worthyPop = []
    sum_nums = [] 
    prod_nums = []
    for item in population:
        summ , prod = caculateFactors(item)
        prod,summ = genetic.utility(summ,prod)
        sum_nums.append(summ)
        prod_nums.append(prod)
    
    pop1 = []
    pop2 = []
    for item in population:
        pop1.append(item)
        pop2.append(item)
    FM.sorter_Writer.append("====================== SUM==========================")
    bubble_sort(sum_nums,pop1)  
    FM.sorter_Writer.append("====================== PROD ==========================")
    bubble_sort(prod_nums,pop2)
    i = 0 
    while i < CR.populationLimit/2 :
        worthyPop.append(pop1[i])
        i += 1
    i = 0 

    for item in pop2 :
        if(len(worthyPop) == CR.populationLimit ):
            break
        if ( not item in worthyPop):           
            worthyPop.append(pop2[i])
            
    return worthyPop


def caculateFactors(child):
    if(CR.debugMode):
        FM.errors_Writer.append("Calculate Factor")
    summation = 0 
    production = 1  
#    print("Len : " + str((child)))
    for chromosome in child:
        summation += chromosome
        production *= chromosome
    return summation,production
  
    
def createRandomParents(parentsLength):
    if(CR.debugMode):
        FM.errors_Writer.append("Create Random Parents")
    mother = []
    father = []
    i = 0 
    while (len(mother) != parentsLength):
        i += 1
        rnd = random.randint(1,10)
        if(not rnd in mother):
            mother.append(rnd)
            
    for i in range (1,11):
        if ( not i in mother ):
            father.append(i)
    return (mother,father)  



def countOverlap(li1 , li2):
    if(CR.debugMode):
        FM.errors_Writer.append("COUNT OVERLAP")
    overlap = 0 
    for item in li1 :
        if(item in li2):
            overlap += 1
    return overlap  




