# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    currentFood=currentGameState.getFood().asList()
    foodPositions=newFood.asList()
    
    eatenByGhost=False
    foodScore=0
    ghostScore=0
    gDis=0
    finalScore=0
    fDisMin=100000
   
    if newPos in currentFood:
      foodScore += 10
    #print len(foodPositions)
    for food in foodPositions:
      fDis=manhattanDistance(newPos,food)
      if fDisMin>fDis:
        fDisMin=fDis
        foodScore +=1 
      if fDis<=3:
        foodScore +=2 
      if fDis==0:
        foodScore +=3
    #print len(newGhostStates)
    for i in range(len(newGhostStates)):
      ghostPosition=newGhostStates[i].getPosition()
      gDis=manhattanDistance(ghostPosition,newPos)
      #print gDis
      if gDis==0:
        eatenByGhost=True
      elif gDis<=5:
        ghostScore -=25./gDis
        #print ghostScore
      if eatenByGhost:
        finalScore -=100
    #print foodScore+ghostScore
    #if eatenByGhost:
      
    return finalScore+foodScore+ghostScore
        

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    return self.expAction(0,gameState)[0]
  def getMax(self,depth,gameState):
    nextActions=gameState.getLegalActions(depth%gameState.getNumAgents())
    maxScore=("Null",-999999)
    for action in nextActions:
      if action==Directions.STOP:
        continue
      else:
        tmp=self.expAction(depth+1,gameState.generateSuccessor(depth%gameState.getNumAgents(), action))
        maxScore=(action,tmp[1]) if tmp[1]>maxScore[1] else maxScore 
    return maxScore

  def getMin(self,depth,gameState):
    nextActions=gameState.getLegalActions(depth%gameState.getNumAgents())
    minScore=("Null",999999)
    for action in nextActions:
      if action==Directions.STOP:
        continue
      tmp=self.expAction(depth+1,gameState.generateSuccessor(depth%gameState.getNumAgents(), action))
      minScore=(action,tmp[1]) if tmp[1]<minScore[1] else minScore 
    return minScore

  def expAction(self, depth, gameState):
    if gameState.isWin() or gameState.isLose() or depth==self.depth* gameState.getNumAgents():
      return ("Null",self.evaluationFunction(gameState))
    if depth%gameState.getNumAgents()==0:
      return self.getMax(depth, gameState)
    else:
      return self.getMin(depth, gameState)

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    return self.expAction(0,gameState, -999999, 999999)[0]
  def getMax(self,depth,gameState, alpha, beta):
    nextActions=gameState.getLegalActions(depth%gameState.getNumAgents())
    maxScore=("Null",-999999)
    for action in nextActions:
      if action==Directions.STOP:
        continue
      tmp=self.expAction(depth+1,gameState.generateSuccessor(depth%gameState.getNumAgents(), action), alpha, beta)
      maxScore=(action,max(tmp[1], maxScore[1])) if tmp[1]>maxScore[1] else maxScore 
      if maxScore[1]>beta: return maxScore
      if maxScore[1]>alpha: alpha=maxScore[1]
    return maxScore

  def getMin(self,depth,gameState, alpha, beta):
    nextActions=gameState.getLegalActions(depth%gameState.getNumAgents())
    minScore=("Null",999999)
    for action in nextActions:
      if action==Directions.STOP:
        continue
      tmp=self.expAction(depth+1,gameState.generateSuccessor(depth%gameState.getNumAgents(), action),alpha, beta)
      minScore=(action,min(tmp[1], minScore[1])) if tmp[1]<minScore[1] else minScore 
      if alpha>minScore[1]: return minScore
      if minScore[1]<beta:
        beta=minScore
    return minScore

  def expAction(self, depth, gameState, alpha, beta):
    if gameState.isWin() or gameState.isLose() or depth==self.depth* gameState.getNumAgents():
      return ("Null",self.evaluationFunction(gameState))
    if depth%gameState.getNumAgents()!=0:
      return self.getMin(depth, gameState, alpha, beta)
    else:
      return self.getMax(depth, gameState, alpha, beta)



class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    return self.expAction(0,gameState)[0]

  def expAction(self, depth, gameState):
    if gameState.isWin() or gameState.isLose() or depth==self.depth* gameState.getNumAgents():
      return ("Null",self.evaluationFunction(gameState))
    if depth%gameState.getNumAgents()==0:
      return self.getMax(depth, gameState)
    else:
      return self.expValue(depth, gameState)

  def getMax(self,depth,gameState):
    nextActions=gameState.getLegalActions(depth%gameState.getNumAgents())

    maxScore=("Null",-999999)
    for action in nextActions:
      if action==Directions.STOP:
        continue
      else:
        tmp=self.expAction(depth+1,gameState.generateSuccessor(depth%gameState.getNumAgents(), action))
        maxScore=(action,max(tmp[1], maxScore[1])) if tmp[1]>maxScore[1] else maxScore 
    return maxScore

  def expValue(self, depth,gameState):
    nextActions=gameState.getLegalActions(depth%gameState.getNumAgents())


    p=1./len(nextActions)
    v=0
    for action in nextActions:
      if action==Directions.STOP:
        continue
      else:
        tmp=self.expAction(depth+1, gameState.generateSuccessor(depth%gameState.getNumAgents(), action))
        v+=p*tmp[1]
    return ("Null",v)



def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  newPos = currentGameState.getPacmanPosition()
  newFood = currentGameState.getFood()
  newGhostStates = currentGameState.getGhostStates()
  newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
  newCapsulPos=currentGameState.getCapsules()
  foods=newFood.asList()
  eatGhost=0
  
  ghostScore=0
  for ghost in newGhostStates:
    gDis=manhattanDistance(newPos,ghost.getPosition())
    if newScaredTimes>0:
      if gDis==0:
        eatGhost+=1
    elif gDis<=2:
        ghostScore-=gDis*1.5 

  foodScore=0
  for food in foods:
    fDis=manhattanDistance(newPos,food)
    length=len(foods)
    foodScore+=0.1/(fDis+100)
    foodScore+=0.3/(length+0.1)

  capsuleScore=0
  for capsule in newCapsulPos:
    cDis=manhattanDistance(newPos,capsule)
    if cDis<=2:
        capsuleScore+=100    

  return ghostScore+foodScore+capsuleScore+1.5*currentGameState.getScore()-10*len(newCapsulPos)-len(newFood.asList())+eatGhost*10


# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

