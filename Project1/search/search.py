# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    from util import Stack
    actionList = []
    state = problem.getStartState()
    action = 'null'
    cost = 0
    parent = state
    dictionary = {state:[action, cost, parent]}
    if problem.isGoalState(problem.getStartState()):
        return actionList
    frontier = Stack()
    frontier.push(state)
    explored = []
    Find_goal = False
    goal_state = state
    
    while not Find_goal:
        if frontier.isEmpty():
            print "DFS fails!!!!!!!!!!!!!!!"
            return actionList
        state = frontier.pop()
        if state in explored:
            continue
        #print '\nexpand the node ', state, 'with successors: '
        explored.append(state)
        if problem.isGoalState(state):
            Find_goal = True
            goal_state = state
            break
        parent_cost = dictionary[state][1]
        for i in problem.getSuccessors(state):
            child_state = i[0]
            #print child_state
            child_action = i[1]
            child_cost = i[2]+parent_cost
            if child_state in explored:
                continue
            '''
            if dictionary.has_key(child_state):
                if dictionary.get(child_state)[1] <= child_cost:
                    continue
            '''
            frontier.push(child_state)
            dictionary[child_state] = [child_action, child_cost, state]
            #print '\nappend the node: ', dictionary[child_state]
            
                
    current = goal_state
    while dictionary[current][0] != 'null':
        actionList.insert(0,dictionary[current][0])
        #print '\n', dictionary[current]
        current = dictionary[current][2]
    
    return actionList
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    from util import Queue
    actionList = []
    state = problem.getStartState()
    action = 'null'
    cost = 0
    parent = state
    dictionary = {state:[action, cost, parent]}
    if problem.isGoalState(problem.getStartState()):
        return actionList
    frontier = Queue()
    frontier.push(state)
    explored = []
    Find_goal = False
    goal_state = state
    
    while not Find_goal:
        if frontier.isEmpty():
            print "BFS fails!!!!!!!!!!!!!!!"
            return actionList
        state = frontier.pop()
        if state in explored:
            continue
        #print '\nexpand the node ', state, 'with successors: '
        explored.append(state)
        if problem.isGoalState(state):
            Find_goal = True
            goal_state = state
            break
        #print 'expand ', state
        parent_cost = dictionary[state][1]
        for i in problem.getSuccessors(state):
            child_state = i[0]
            #print child_state
            child_action = i[1]
            child_cost = i[2]+parent_cost
            if child_state in explored:
                continue
            if dictionary.has_key(child_state):
                if dictionary.get(child_state)[1] <= child_cost:
                    continue
            dictionary[child_state] = [child_action, child_cost, state]
            
            frontier.push(child_state)
            #print '\npush ', child_state
            
            #print '\nappend the node: ', dictionary[child_state]
                
    current = goal_state
    while dictionary[current][0] != 'null':
        actionList.insert(0,dictionary[current][0])
        current = dictionary[current][2]
    
    return actionList
    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    actionList = []
    state = problem.getStartState()
    action = 'null'
    cost = 0
    parent = state
    dictionary = {state:[action, cost, parent]}
    if problem.isGoalState(problem.getStartState()):
        return actionList
    frontier = PriorityQueue()
    frontier.push(state, cost)
    explored = []
    Find_goal = False
    goal_state = state
    
    while not Find_goal:
        if frontier.isEmpty():
            print "UCS fails!!!!!!!!!!!!!!!"
            return actionList
        state = frontier.pop()
        #print '\nexpand the node ', state, 'with successors: '
        if problem.isGoalState(state):
            Find_goal = True
            goal_state = state
            break
        explored.append(state)
        parent_cost = dictionary[state][1]
        for i in problem.getSuccessors(state):
            child_state = i[0]
            #print child_state
            child_action = i[1]
            child_cost = i[2]+parent_cost
            if child_state in explored:
                continue
            if dictionary.has_key(child_state):
                if dictionary.get(child_state)[1] <= child_cost:
                    continue
            frontier.push(child_state, child_cost)
            dictionary[child_state] = [child_action, child_cost, state]
            #print '\nappend the node: ', dictionary[child_state]
                
    current = goal_state
    while dictionary[current][0] != 'null':
        actionList.insert(0,dictionary[current][0])
        current = dictionary[current][2]
    
    return actionList
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    actionList = []
    state = problem.getStartState()
    action = 'null'
    cost = 0
    h = heuristic(state, problem)
    parent = state
    dictionary = {state:[action, cost, parent, h]}
    if problem.isGoalState(problem.getStartState()):
        return actionList
    frontier = PriorityQueue()
    frontier.push(state, h)
    explored = []
    Find_goal = False
    goal_state = state
    
    while not Find_goal:
        if frontier.isEmpty():
            print "DFS fails!!!!!!!!!!!!!!!"
            return actionList
        state = frontier.pop()
        if state in explored:
            continue
        #print '\nexpand the node ', state, 'with successors: '
        explored.append(state)
        if problem.isGoalState(state):
            Find_goal = True
            goal_state = state
            break
        parent_cost = dictionary[state][1]
        for i in problem.getSuccessors(state):
            child_state = i[0]
            #print child_state
            child_action = i[1]
            child_cost = i[2]+parent_cost
            child_h = heuristic(child_state, problem)
            if child_state in explored:
                continue
            if dictionary.has_key(child_state):
                if dictionary.get(child_state)[1] <= child_cost:
                    continue
            frontier.push(child_state, child_h+child_cost)
            dictionary[child_state] = [child_action, child_cost, state, child_h]
            #print '\nappend the node: ', dictionary[child_state]
                
    current = goal_state
    while dictionary[current][0] != 'null':
        actionList.insert(0,dictionary[current][0])
        current = dictionary[current][2]
    
    return actionList
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
