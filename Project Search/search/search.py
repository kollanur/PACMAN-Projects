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

class Node:
  def __init__(self):
    self.parentNode = None
    self.act        = None
    self.co         = None 

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
    """
    #print("Start:", problem.getStartState())
    #print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    #print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    
    actionList = []
    length = 1
    tempState = None
    presentState = problem.getStartState()
    if isinstance(presentState,list):
      tempState = presentState[0]
      length=4
    else:
      tempState = presentState
    expanded_nodes = {None}
    fringe = util.Stack()
    root = Node()
    root.parentNode = -1
    for x in range(length):
      presentState = tempState
      path = {}
      path[presentState] = root
      while True:
        if presentState not in expanded_nodes:
          expanded_nodes.add(presentState)
          if problem.isGoalState(presentState):
            tempState = presentState
            while True:
              if path[presentState].parentNode == -1:
                break
              else:
                actionList.append(path[presentState].act)
                presentState = path[presentState].parentNode
            break
          for newNode, move, cos in problem.getSuccessors(presentState):
            if newNode not in expanded_nodes: 
              nod = Node()
              nod.parentNode = presentState
              nod.act        = move
              fringe.push(newNode)
              path[newNode] = nod
        presentState = fringe.pop()
    actionList.reverse()
    return actionList

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    actionList = []
    tempState = None
    length = 1
    root = Node()
    root.parentNode = -1
    path = {}
    presentState = problem.getStartState()
    if isinstance(presentState, list):
      tempState = presentState[0]
      length = 4
    else:
      tempState = presentState
    start = tempState
    #expanded_nodes = {None}
    #visited_nodes = {tempState}
    finalList = []
    for x in range(length):
      actionList = []
      fringe = util.Queue()
      path ={}
      presentState = tempState
      path[presentState] = root
      visited_nodes = {presentState}
      expanded_nodes = {None}
      while True:
        if presentState not in expanded_nodes:
          expanded_nodes.add(presentState)
          if problem.isGoalState(presentState):
            tempState = presentState
            while True:
              if path[presentState].parentNode == -1:
                actionList.reverse()
                for x in actionList:
                  finalList.append(x)
                break
              else:
                actionList.append(path[presentState].act)
                presentState = path[presentState].parentNode
            break
          for newNode, move, cos in problem.getSuccessors(presentState):
            if newNode not in visited_nodes:
              visited_nodes.add(newNode)
              nod = Node()
              nod.parentNode = presentState
              nod.act = move
              path[newNode] = nod
              fringe.push(newNode)
        presentState = fringe.pop()
    return finalList
  
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    root = Node()
    root.parentNode = -1
    root.co = 0
    actionList = []
    presentState = problem.getStartState()
    if isinstance(presentState, list):
      presentState = presentState[0]
    path = {}
    path[presentState] = root
    expanded_nodes = {None}
    fringe = util.PriorityQueue()
    while True:
      if presentState not in expanded_nodes:
        expanded_nodes.add(presentState)
        if problem.isGoalState(presentState):
          while True:
            if path[presentState].parentNode == -1:
              break
            else:
              actionList.append(path[presentState].act)
              presentState = path[presentState].parentNode
          break
        for newNode, move, cos in problem.getSuccessors(presentState):
            nod = Node()
            nod.parentNode = presentState
            nod.act = move
            if newNode in path:
              if path[newNode].co > cos + path[presentState].co:
                nod.co = cos + path[presentState].co
                path[newNode] = nod
                fringe.update(newNode, cos + path[presentState].co)
            else:
              nod.co  = cos + path[presentState].co
              path[newNode] = nod
            fringe.push(newNode, cos+path[presentState].co)
      presentState = fringe.pop()
    actionList.reverse()
    return actionList

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    presentState = problem.getStartState()
    if isinstance(presentState, list):
      presentState = presentState[0]
    root = Node()
    root.parentNode = -1
    root.co = 0
    actionList = []
    path = {}
    path[presentState] = root
    expanded_nodes = {None}
    fringe = util.PriorityQueue()
    while True:
      if presentState not in expanded_nodes:
        expanded_nodes.add(presentState)
        if problem.isGoalState(presentState):
          while True:
            if path[presentState].parentNode == -1:
              break
            else:
              actionList.append(path[presentState].act)
              presentState = path[presentState].parentNode
          break
        for newNode, move, cos in problem.getSuccessors(presentState):
          nod = Node()
          nod.parentNode = presentState
          nod.act = move
          if newNode in path:
            if path[newNode].co > cos + path[presentState].co:
              nod.co = cos + path[presentState].co
              path[newNode] = nod
              fringe.update(newNode, cos + path[presentState].co + heuristic(newNode, problem))
          else:
            nod.co = cos + path[presentState].co
            fringe.push(newNode, cos + path[presentState].co + heuristic(newNode, problem))
            path[newNode] = nod
      presentState = fringe.pop()
    actionList.reverse()
    return actionList    


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
