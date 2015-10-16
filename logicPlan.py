# logicPlan.py
# ------------
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
In logicPlan.py, you will implement logic planning methods which are called by
Pacman agents (in logicAgents.py).
"""

import util
import sys
import logic
import game


pacman_str = 'P'
ghost_pos_str = 'G'
ghost_east_str = 'GE'
pacman_alive_str = 'PA'

class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined()

def tinyMazePlan(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def sentence1():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    A = logic.Expr('A')
    B = logic.Expr('B')
    C = logic.Expr('C')
    aaa = logic.disjoin(A,B)
    a_or_b = ~A % (~B | C)
    not_a = logic.disjoin(~A,~B,C)
    return logic.conjoin(aaa,a_or_b,not_a)




def sentence2():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    A = logic.Expr('A')
    B = logic.Expr('B')
    C = logic.Expr('C')
    D = logic.Expr('D')
    aaa = C % (B | D)
    a_or_b = A >> (~B & ~D)
    not_a = ~(B & ~C) >> A
    not_d = ~D >> C
    return logic.conjoin(aaa,a_or_b,not_a,not_d)


def sentence3():
    """Using the symbols WumpusAlive[1], WumpusAlive[0], WumpusBorn[0], and WumpusKilled[0],
    created using the logic.PropSymbolExpr constructor, return a logic.PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    The Wumpus is alive at time 1 if and only if the Wumpus was alive at time 0 and it was
    not killed at time 0 or it was not alive and time 0 and it was born at time 0.

    The Wumpus cannot both be alive at time 0 and be born at time 0.

    The Wumpus is born at time 0.
    """
    a = logic.PropSymbolExpr("WumpusAlive[1]")
    b = logic.PropSymbolExpr("WumpusAlive[0]")
    c = logic.PropSymbolExpr("WumpusBorn[0]")
    d = logic.PropSymbolExpr("WumpusKilled[0]")
    alive = a % ((b & ~d) | (~b & c))
    cant = ~(b & c)
    born = c
    return logic.conjoin(alive,cant,born) 



def findModel(sentence):
    """Given a propositional logic sentence (i.e. a logic.Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    # print sentence
    a = logic.to_cnf(sentence)
    
    b = logic.pycoSAT(a)
    return b

def atLeastOne(literals) :
    """
    Given a list of logic.Expr literals (i.e. in the form A or ~A), return a single 
    logic.Expr instance in CNF (conjunctive normal form) that represents the logic 
    that at least one of the literals in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    return logic.disjoin(literals)


def atMostOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form) that represents the logic that at most one of 
    the expressions in the list is true.
    """
    conjunctions = []
    for literal in literals:
        not_literal = ~literal

        # Disjoin literal with NOT(literal) for every other element besides this literal
        # and add it to the list to be conjoined
        for inner_literal in literals:
            if literal != inner_literal:
                not_inner_literal = ~inner_literal
                disjunction = logic.disjoin(not_literal, not_inner_literal)
                conjunctions.append(disjunction)

    return logic.conjoin(conjunctions)


def exactlyOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form)that represents the logic that exactly one of 
    the expressions in the list is true.
    """
    # print literals
    conjunctions = []
    one_must_be_true_list = []
    for literal in literals:
        not_literal = ~literal
        one_must_be_true_list.append(literal)

        # Disjoin literal with NOT(literal) for every other element besides this literal
        # and add it to the list to be conjoined
        for inner_literal in literals:
            if literal != inner_literal:
                not_inner_literal = ~inner_literal
                disjunction = logic.disjoin(not_literal, not_inner_literal)
                conjunctions.append(disjunction)

    # Add the expression that states at least one of the literals must be true
    one_must_be_true = logic.disjoin(one_must_be_true_list)
    conjunctions.append(one_must_be_true)

    return logic.conjoin(conjunctions)


def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    models = []
    final = []
    for i in model.keys():
        if model[i]:
            a = logic.PropSymbolExpr.parseExpr(i)
            if a[0] in actions:
                models.append(a)
    p = sorted(models, key=lambda mod: int(mod[1]))
    for m in p:
        final.append(m[0])
    return final

def pacmanSuccessorStateAxioms(x, y, t, walls_grid):
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a 
    grid representing the wall locations).
    Current <==> (previous position at time t-1) & (took action to move to x, y)
    """
    current = logic.PropSymbolExpr(pacman_str, x, y, t)

    neighbors = []

    if walls_grid[x-1][y] == False:
        prev_position = logic.PropSymbolExpr(pacman_str, x-1, y, t-1)
        action = logic.PropSymbolExpr('East', t-1)
        state = logic.conjoin(prev_position, action)
        neighbors.append(state)

    if walls_grid[x+1][y] == False:
        prev_position = logic.PropSymbolExpr(pacman_str, x+1, y, t-1)
        action = logic.PropSymbolExpr('West', t-1)
        state = logic.conjoin(prev_position, action)
        neighbors.append(state)

    if walls_grid[x][y-1] == False:
        prev_position = logic.PropSymbolExpr(pacman_str, x, y-1, t-1)
        action = logic.PropSymbolExpr('North', t-1)
        state = logic.conjoin(prev_position, action)
        neighbors.append(state)

    if walls_grid[x][y+1] == False:
        prev_position = logic.PropSymbolExpr(pacman_str, x, y+1, t-1)
        action = logic.PropSymbolExpr('South', t-1)
        state = logic.conjoin(prev_position, action)
        neighbors.append(state)

    prev_states = atLeastOne(neighbors)
    final_axiom = current % prev_states
    # print final_axiom
    return final_axiom


def positionLogicPlan(problem):
    """
    Given an instance of a PositionPlanningProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    # print walls.asList()

    MAX_TIME_STEP = 50
    actions = ['North', 'East', 'South', 'West']
    width, height = problem.getWidth(), problem.getHeight()
    initial_state = problem.getStartState()
    current = logic.PropSymbolExpr(pacman_str, initial_state[0], initial_state[1], 0)
    goal_state = problem.getGoalState()
    expression = list()

    for x in range(1, width + 1) :
        for y in range(1, height + 1) :
            if (x, y) == initial_state:
                if expression:
                    v = expression.pop()
                    expression.append(logic.conjoin(v,logic.PropSymbolExpr("P", x, y, 0)))
                else:
                    expression.append(logic.Expr("~", logic.PropSymbolExpr("P", x, y, 0)))
            else :
                if expression:
                    v = expression.pop()
                    expression.append(logic.conjoin(v,logic.Expr("~", logic.PropSymbolExpr("P", x, y, 0))))
                else:
                    expression.append(logic.Expr("~", logic.PropSymbolExpr("P", x, y, 0)))
    initial = expression[0]
    # print initial
    successors = []
    exclusion = []
    for t in range(3):
        for x in range(1, width + 1):
            for y in range(1, height + 1):
                if (x, y) not in walls.asList():
                    n = []
                    if t > 0:
                        successors += [pacmanSuccessorStateAxioms(x, y, t, walls)]
                        for action in actions:
                            exclusion.append(logic.PropSymbolExpr(action, t-1))
                        n = exactlyOne(exclusion)
                    # print n
                    # print "     "
                    suc = logic.conjoin(successors)
                    # print suc
                    # print "     "
                    goal = pacmanSuccessorStateAxioms(goal_state[0], goal_state[1], t + 1, walls)
                    # print goal
                    # print "     "
                    if n and successors:
                        j = findModel(logic.conjoin(initial, goal, suc, n))
                    else:
                        print "hi"
                        j = findModel(logic.conjoin(initial, goal))
                    print j
                    # return None
                    if j is True:
                        return extractActionSequence(j, actions)
    return None

def foodLogicPlan(problem):
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()

    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def ghostPositionSuccessorStateAxioms(x, y, t, ghost_num, walls_grid):
    """
    Successor state axiom for patrolling ghost state (x,y,t) (from t-1).
    Current <==> (causes to stay) | (causes of current)
    GE is going east, ~GE is going west 
    """
    pos_str = ghost_pos_str+str(ghost_num)
    east_str = ghost_east_str+str(ghost_num)
    current = logic.PropSymbolExpr(pos_str, x, y, t)

    neighbors = []

    if walls_grid[x-1][y] == False:
        prev_position = logic.PropSymbolExpr(pos_str, x-1, y, t-1)
        action = logic.PropSymbolExpr(east_str, t-1)
        state = logic.conjoin(prev_position, action)
        neighbors.append(state)

    if walls_grid[x+1][y] == False:
        prev_position = logic.PropSymbolExpr(pos_str, x+1, y, t-1)
        action = ~logic.PropSymbolExpr(east_str, t-1)
        state = logic.conjoin(prev_position, action)
        neighbors.append(state)

    prev_states = atLeastOne(neighbors)
    if str(prev_states) == "FALSE":
        final_axiom = current % logic.PropSymbolExpr(pos_str, x, y, t-1)
    else:
        final_axiom = current % prev_states
    return final_axiom

def ghostDirectionSuccessorStateAxioms(t, ghost_num, blocked_west_positions, blocked_east_positions):
    """
    Successor state axiom for patrolling ghost direction state (t) (from t-1).
    west or east walls.
    Current <==> (causes to stay) | (causes of current)
    """
    pos_str = ghost_pos_str+str(ghost_num)
    east_str = ghost_east_str+str(ghost_num)

    neighbors = []
    to_join = []
    n1 = blocked_west_positions[:]
    p1 = blocked_east_positions[:]
    dont = []
    wont = []
    hont = []
    while n1:
        a = n1.pop()
        dont += [logic.PropSymbolExpr(pos_str, a[0], a[1], t)]
        hont += [~logic.PropSymbolExpr(pos_str, a[0], a[1], t)]
    while p1:
        a = p1.pop()
        wont += [~logic.PropSymbolExpr(pos_str, a[0], a[1], t)]
        hont += [~logic.PropSymbolExpr(pos_str, a[0], a[1], t)]

    #make sure ghost is not in positions where it is blocked to the right
    wont = logic.conjoin(wont)
    tont = logic.conjoin(dont)
    dont = logic.disjoin(dont)
    hont = logic.conjoin(hont)
    sont = logic.conjoin(wont, tont)
    jont = ~logic.conjoin(hont, ~logic.PropSymbolExpr(east_str, t-1))
    m = logic.disjoin(wont, dont)
    h = logic.conjoin(wont, dont)
    k = logic.conjoin(m, ~logic.PropSymbolExpr(east_str, t-1))
    l = logic.disjoin(k, logic.conjoin(h, logic.PropSymbolExpr(east_str, t-1)), logic.conjoin(hont, logic.PropSymbolExpr(east_str, t-1)))
    b = logic.conjoin(l, jont)
    final_axiom = logic.PropSymbolExpr(east_str, t) % b
    return final_axiom
    # return logic.Expr('A') 


def pacmanAliveSuccessorStateAxioms(x, y, t, num_ghosts):
    """
    Successor state axiom for patrolling ghost state (x,y,t) (from t-1).
    Current <==> (causes to stay) | (causes of current)
    """
    ghost_strs = [ghost_pos_str+str(ghost_num) for ghost_num in xrange(num_ghosts)]
    current = logic.PropSymbolExpr(pacman_str, x, y, t)
    ghosts = ghost_strs[:]
    neighbors = []

    k = []
    l = []
    while num_ghosts != 0:
        k += [logic.conjoin(logic.PropSymbolExpr(pacman_str, x, y, t), logic.PropSymbolExpr(ghost_strs[num_ghosts-1], x, y, t))]
        l += [logic.conjoin(logic.PropSymbolExpr(pacman_str, x, y, t), logic.PropSymbolExpr(ghost_strs[num_ghosts-1], x, y, t-1))]
        num_ghosts -= 1
    m = ~logic.PropSymbolExpr(pacman_alive_str, t-1)

    prev_states = logic.disjoin(logic.disjoin(k), logic.disjoin(l), m)
    final_axiom = ~logic.PropSymbolExpr(pacman_alive_str, t) % prev_states
    return final_axiom

def foodGhostLogicPlan(problem):
    """
    Given an instance of a FoodGhostPlanningProblem, return a list of actions that help Pacman
    eat all of the food and avoid patrolling ghosts.
    Ghosts only move east and west. They always start by moving East, unless they start next to
    and eastern wall. 
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()

    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan
fglp = foodGhostLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)
    