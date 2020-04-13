# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions
from pacman import Actions as pacmanActions
from pacman import PacmanRules as pacmanrules


s = Directions.SOUTH
w = Directions.WEST
n = Directions.NORTH
e = Directions.EAST

""" My OWN Class for Analyzing the Consistency of Heuristic used in A* Method """

class Analyzer :
    """
    This class is implemented to check whether the path chosen by A* heuristic is consistent or not.
    @actions : returned actions by A* method which then  will be converted to @corndinates

    
    @coordinates :  the tranlsateion of each action from @actions in cordinate form of (x,y) that determines which way to go.
                    for example corrdinate:(-1,0) means that pacman should go one step to "west"
    
    @states : the states that exists in the path of pacman. These states are created by using start state of pacman and @coordinates

    """
    foodCoordinates = []
    X = 0
    foodGridShit = None
    def __init__(self , problem , actions ):
        self.problem = problem
        self.startState = problem.getStartState()
        self.actions = actions
        self.coordinates = []
        self.states = []
        self.path = []
        
    #the double underscore __ means the method is private
    def __findFoodOrdering(self):
        for node in self.states :
            if( (node in self.foodCoordinates) and (not node in self.path) ):
                self.path.append(node)
                
    def __createStates(self):
        for action in self.actions :
            vector = pacmanActions.directionToVector( action, pacmanrules.PACMAN_SPEED )
            self.coordinates.append(vector)
        self.states.append(self.startState)
        for coordinate in self.coordinates:
            xCord , yCord = coordinate
            try:
                currentCordX , currentCordY = self.states[-1][0]  
            except:
                currentCordX , currentCordY = self.states[-1]
            #print(str(currentCordX) + "|" + str(currentCordY))
            nextCordX = xCord + int(currentCordX)
            nextCordY = yCord + int(currentCordY)
            newState = (nextCordX,nextCordY)
            self.states.append(newState)
    
    def __analyze(self):
        for state in self.states :
            if(len(self.path) > 0 ):
                nextGoal = self.path[0]
                if(state == nextGoal):
                    self.path.remove(state)
                    if(len(self.path) > 0 ):
                        nextGoal = self.path[0]
                        tempSearchState = state , Analyzer.foodGridShit
                        stateSuccessors = self.problem.getSuccessors(tempSearchState)
                        sumOfManhattans = 0 
                        for successor in stateSuccessors :
                            successorState , action , cost = successor
                           # print(successorState)
                           #print(nextGoal)
                            sumOfManhattans += util.manhattanDistance(successorState[0],nextGoal)
                        currentStateManhattanDistance = util.manhattanDistance(state,nextGoal)
                        if ( currentStateManhattanDistance <= sumOfManhattans + 3):
                            True
                        else:
                            return False
        return True
    
    def __isConsistent(self):
        isConsistent = self.__analyze()
        if(isConsistent):
            print("It's Consistent")
            return True
        print("Not Consistent")
        return False
    
    def start(self):
        print("========== Analyzer Data ============")
        self.__createStates()
        self.__findFoodOrdering()
        self.__printData()
        self.__isConsistent()
        print("=======================")
    
    def __printData(self):
        print("Actions : " + str(self.actions))
        print("Cordinates : " + str(self.coordinates))
        print("States : " + str(self.states))
        print("Food Coordinates : " + str(Analyzer.foodCoordinates))
        print("Path: " + str(self.path))
        
    # Static functions of this class
    # createStates = staticmethod(createStates)
    # printData = staticmethod(printData)

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
        
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    #print("Hello Hossein")
    startState = problem.getStartState()
    visitedNodes = []
    actions = []
    fringe = util.Stack()
    cost = 0 
    #print("Start State : "  , startState);
    if (problem.isGoalState(startState) == True):#if startState is the goalState
        return actions
    else :
        # Data Type Format : (currentState,actions,cost) based on errors I got ;\
        fringe.push((startState,actions,cost))
        while (fringe.isEmpty() == False) :
            currentState , actions , cost = fringe.pop()
            #print("Current State : " + str(currentState))
            #print(actions)
            if(problem.isGoalState(currentState)):
                return actions
            
            elif ((currentState in visitedNodes) == False ):
                visitedNodes.append(currentState)
                currentNodeSuccessors = problem.getSuccessors(currentState)
                #print("Current Node Successors : " + str(currentNodeSuccessors))
                for node in currentNodeSuccessors :
                    state , action , cost = node
                    if ( (state in visitedNodes) == False ):
                        newNode = (state , actions + [action] , cost)
                        fringe.push(newNode)
                    
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"  
    print("Processing...")
    startState = problem.getStartState()
    visitedNodes = []
    fringe = util.Queue()
    cost = 0     
    if (problem.isGoalState(startState) == True ):
        return [] # No Specific Actions
    else :
        fringe.push((startState , [] , cost ))
        while ( fringe.isEmpty() == False ):
            currentState , actions , cost = fringe.pop()
            """ get the latest node in the Queue """
            
            if ( problem.isGoalState(currentState) == True ): 
                """ check if the node is our goal or not """
                #print("We Reached Goal")
                #print("Final Path : " + str(actions))
                return actions
            else:
                if ( (currentState in visitedNodes) == False ):  
                    """ check if this node is alreay visited or needs to be extended ? """
                    visitedNodes.append(currentState)
                    currentNodeSuccessors = problem.getSuccessors(currentState)
                    for node in currentNodeSuccessors :
                        if(not node in visitedNodes):
                            state , action , cost = node 
                            if ( not state in visitedNodes):
                                fringe.push((state , actions + [action] , cost ))
                                #print(str(actions + [action]))   
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    fringe = util.PriorityQueue()
    cost = 0 
    visitedNodes = []
    actions = []
    
    """ 
    Format of Priority Queue :
        (item , priority)
        item => state , actions , cost
    priorityQueue.push ( (state , actions , cost) , cost )
    
    """
    
    if ( problem.isGoalState(startState) ):
        return actions
    else :
        newNode = startState , actions , cost
        priority = cost
        fringe.push( newNode , priority )
        while ( fringe.isEmpty() == False ):
            currentState , actions , cost = fringe.pop()
            if ( problem.isGoalState(currentState) == True ) : 
                return actions
            else :
                if ( (currentState in visitedNodes) == False ):
                    visitedNodes.append(currentState)
                    currentStateSuccessors = problem.getSuccessors(currentState)
                    for node in currentStateSuccessors :
                        state , action , stateCost = node
                        if( ( state in visitedNodes) == False ) :
                            newNode = state , actions + [action] , cost + stateCost
                            priority = cost + stateCost
                            fringe.push( newNode , priority )
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    print("Processing...")
    
    startState = problem.getStartState();
    fringe = util.PriorityQueue()
    costs = 0 
    visitedNodes = []
    actions = [] 
    if ( problem.isGoalState(startState) == True):
        return actions
    else:
        newFringeItem = (startState , actions , costs)
        fringe.push(newFringeItem,costs)
        while(fringe.isEmpty() == False ):
            #f(x) = h(x) + g(x)
            currentState , actions , costs = fringe.pop()
            if ( problem.isGoalState(currentState) == True):
                #print("Final Actions : " + str(actions))       
                """Start :  Analyzer Properties """
                analyzer = Analyzer(problem,actions)
                analyzer.start()
                
                
                #Analyzer.printData()
                """End : Analyzer Properties """
                return actions
            else:
                if(not currentState in visitedNodes ):
                    visitedNodes.append(currentState)
                    currentNodeSuccessors = problem.getSuccessors(currentState)
                    for node in currentNodeSuccessors :
                        state , action , stateCost = node
                        heuristicAmount = heuristic(state , problem)
                        newFringeItem = state , actions + [action] , costs + stateCost
                        priority = costs + heuristicAmount
                        fringe.push( newFringeItem , priority )
                             
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
