import random
import math
from ExternalLibraries.Writer import Writer as Writer
import os
class ControlRoom:
    #Static Arrtibutes
    projectFilesDirectory = ""
    succeededSumParents = []
    succeededProdParents = []
    population = []
    goalProduct = 360
    goalSummation = 36
    parentsLength = 5 
    generationCounter = 0
    haltsLimit = 30
    debugMode = False
   
    # What You may want to change :
    testCaseNo = 10
    chooseBestNVersion = 1
    populationLimit = 100
    mutationProbability = 40
    
    @classmethod
    def restart(self):
        ControlRoom.population = []
        ControlRoom.succeededSumParents = []
        ControlRoom.succeededProdParents = []
    
    def setFilesPath(path):
        ControlRoom.projectFilesDirectory = path


class FileManager :
    complete_Writer = None
    sorter_Writer = None
    errors_Writer = None
    testCase_Writer = None


def bubble_sort(nums,pop):
    if(ControlRoom.debugMode):
         FileManager.errors_Writer.append("BUBBLE SORT")
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
               
    FileManager.sorter_Writer.append("IT : \n %s" % (ControlRoom.generationCounter) )           
    FileManager.sorter_Writer.append(nums)
    FileManager.sorter_Writer.append(pop)



def findIntersection(c1,c2):
    if(ControlRoom.debugMode):
         FileManager.errors_Writer.append("FIND INTERSECTION")
    for i in c1 :
        if(i in c2):
            return c2.index(i)
    return -1


def haveIntersection(children):
    if(ControlRoom.debugMode):
         FileManager.errors_Writer.append("Hvae Intersection")
    for item in children[0]:
        if(item in children[1]):
            return True
    return False



def sameTwoChildren(childOne , childTwo):
    if(ControlRoom.debugMode):
        FileManager.errors_Writer.append("Same Two Children")
    appearance = 0 
    for item in childOne :
        if ( not item in childTwo ):
            return False
        appearance += 1
    if ( appearance == len(childOne)):
        return True
    return False



    


def caculateFactors(child):
    if(ControlRoom.debugMode):
         FileManager.errors_Writer.append("Calculate Factor")
    summation = 0 
    production = 1  
#    print("Len : " + str((child)))
    for chromosome in child:
        summation += chromosome
        production *= chromosome
    return summation,production
  
    
def createRandomParents(parentsLength):
    if(ControlRoom.debugMode):
         FileManager.errors_Writer.append("Create Random Parents")
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
    ControlRoom.population.append(mother)
    ControlRoom.population.append(father)
    return (mother,father)  



def countOverlap(li1 , li2):
    if(ControlRoom.debugMode):
         FileManager.errors_Writer.append("COUNT OVERLAP")
    overlap = 0 
    for item in li1 :
        if(item in li2):
            overlap += 1
    return overlap  

def sigmoid(x):  
    return (  1 / ( 1 + math.exp( x * -1 ) )  )
    
def scale(y):
    # give me product number
    return y/3.93
        
def saveFig(plotPointer , figName , figNumbPath ):
    filerIO = Writer(figNumbPath)
    lines = filerIO.readFile()
    if ( len(lines) == 0 ):
        filerIO.append(1) 
        lines[0] = 1 
    plotPointer.savefig( str(figName) + str(lines[0]) + '.png')
    filerIO.clearFile()
    filerIO.append(str(int(lines[0]) + 1) ) 

def createNewDirectory(folderBaseName,foldNumbPath):
    filerIO = Writer(foldNumbPath)
    lines = filerIO.readFile()
    if ( len(lines) == 0 ):
        filerIO.append(1)        
        lines[0] = 1
    os.mkdir( "Plots/" + str(folderBaseName) +" " +str(lines[0]) + "  V" +  str(ControlRoom.chooseBestNVersion))   
    ControlRoom.projectFilesDirectory = "Plots/" + str(folderBaseName) +" " +str(lines[0]) + "  V" +  str(ControlRoom.chooseBestNVersion)
    filerIO.clearFile()
    filerIO.append(str(int(lines[0]) + 1) ) 