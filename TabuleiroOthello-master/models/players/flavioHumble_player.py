class Player:

  class Move:
    def __init__(self, x, y):
      self.x = x
      self.y = y

    def __str__(self):
      ret =  self.x.__str__()
      ret += " "
      ret += self.y.__str__()
      return ret

    def __eq__(self, other):
      return (self and other and self.x == other.x and self.y == other.y)

  class HumbleMove:

    def __init__(self, x=None,y=None, nPieces=None):
      self.mX = x
      self.mY = y
      self.mNPieces = nPieces
      return

  class No:
  
    def __init__(self, move = None, parent = None):
      self.mChildren = dict()
      self.mMove = move
      self.mParent = parent
      self.state = "unexplored"
      if parent != None:
        self.depth = parent.depth + 1
      else:
        self.depth = 0
      if(move != None):
        self.mMinScore = move.mNPieces
        self.mMaxScore = move.mNPieces
      else:
        self.mMinScore = 1000000
        self.mMaxScore = 0
      return
        
    def setChild(self, child_id, child_node):
      if(child_id > -1 and child_id < 65 and child_node != None):
        data = {child_id : child_node }
        self.mChildren.update(data)
        if (child_node.mMove.mNPieces < self.mMinScore):
          self.mMinScore = child_node.mMove.mNPieces
          if(self.mParent != None):
            self.mParent.mMinScore = self.mMinScore
        if (child_node.mMove.mNPieces > self.mMaxScore):
          self.mMaxScore = child_node.mMove.mNPieces
          if(self.mParent != None):
            self.mParent.mMaxScore = self.mMaxScore
      return

    def getMinMaxFromChildren(self,getMaxFromMin):
      maxScore = 0
      minScore = 100000
      if len(self.mChildren) == 0:
        if getMaxFromMin:
          return self.mMaxScore
        else:
          return self.mMinScore
      for key in self.mChildren:
        if getMaxFromMin:
          if(self.mChildren[key].mMaxScore > maxScore):
            maxScore = self.mChildren[key].mMaxScore
        else:
          if(self.mChildren[key].mMinScore < minScore):
            minScore = self.mChildren[key].mMinScore
      if getMaxFromMin:
        return maxScore
      else:
        return minScore

  mTotalMovesAhead = 20
  mCornerBias = 10
  mRegion4Bias = -5
  mEdgeBias = 5
  mMovesAhead = 0

  def __init__(self, color):
    self.color = color

  def play(self, board):
    self.simMovesInit(board)
    bestHumbleMove = self.findBestMoveInit()
    if bestHumbleMove != None:
      bestMove = self.Move(bestHumbleMove.mX+1, bestHumbleMove.mY+1)
      return bestMove
    else:
      return None
    
  def simMovesInit (self,board):

    self.mRoot = self.No()

    self.mMovesAhead = 0

    moves = board.valid_moves(self.color)

    if len(moves) > 0:
   
      self.simMoves(self.mRoot,moves,board.get_clone(),self.color,board._opponent(self.color))
    return

  def simMoves(self, root, moves, aMatrix, playerA, playerB):

  
    
    self.mMovesAhead += 1

    if self.mMovesAhead <= self.mTotalMovesAhead:
      
      for aMove in moves:

        #Make a copy of the game board.
        tempMatrix = aMatrix.get_clone()

        #Make a possible prospective move.
        #Flip the simulated pieces for the move.
        tempMatrix.play(aMove,playerA)

        #white
        nPieces = 0
        if(self.color == 'o'):
          nPieces = tempMatrix.score()[0]
        #black
        else:
          nPieces = tempMatrix.score()[1]
        move = self.HumbleMove(aMove.x-1, aMove.y-1, nPieces)
        aNode = self.No(move, root)
        
        root.setChild((move.mX*8)+move.mY,aNode)
        #Simulate the opponent's possible counter moves.
        tempMoves = tempMatrix.valid_moves(playerB)
        if len(tempMoves) > 0:
          self.simMoves(aNode,tempMoves,tempMatrix,playerB,playerA)

    return

  def findBestMoveInit(self):
    self.mMinMaxTree = [self.mRoot]
    bestMove = None
    children = self.mRoot.mChildren
    if len(children) > 0:
      self.findBestMove(self.mRoot)

      #Now get the max from the root's children
      bestIndex = 0
      first = True
      for i in children:

        #Bias is imposed here to simulate more strategic behavior.  Occupying corners and
        #edges of the game board often lead to strategic advantages in the game.

        if (children[i].mMove.mX == 0 and children[i].mMove.mY == 0) or (children[i].mMove.mX == 0 and children[i].mMove.mY == 7) or (children[i].mMove.mX == 7 and children[i].mMove.mY == 0) or (children[i].mMove.mX == 7 and children[i].mMove.mY == 7):
          #Highest bias toward corners.
          children[i].mMaxScore = children[i].mMaxScore + self.mCornerBias
        elif (children[i].mMove.mX == 1 and children[i].mMove.mY == 0) or (children[i].mMove.mX == 0 and children[i].mMove.mY == 1) or (children[i].mMove.mX == 1 and children[i].mMove.mY == 1) or (children[i].mMove.mX == 6 and children[i].mMove.mY == 0) or (children[i].mMove.mX == 7 and children[i].mMove.mY == 1) or (children[i].mMove.mX == 6 and children[i].mMove.mY == 1) or (children[i].mMove.mX == 0 and children[i].mMove.mY == 6) or (children[i].mMove.mX == 1 and children[i].mMove.mY == 7) or (children[i].mMove.mX == 1 and children[i].mMove.mY == 6) or (children[i].mMove.mX == 7 and children[i].mMove.mY == 6) or (children[i].mMove.mX == 6 and children[i].mMove.mY == 7) or (children[i].mMove.mX == 6 and children[i].mMove.mY == 6):
          #Bias against Region4.
          children[i].mMaxScore = children[i].mMaxScore + self.mRegion4Bias
        elif (children[i].mMove.mX == 0) or (children[i].mMove.mX == 7) or (children[i].mMove.mY == 0) or (children[i].mMove.mY == 7):
          #Lower bias toward edges.
          children[i].mMaxScore = children[i].mMaxScore + self.mEdgeBias
        
        if first:
          first = False
          bestIndex = i
        else:
          if children[i].mMaxScore > children[bestIndex].mMaxScore:
            bestIndex = i
      bestMove = children[bestIndex].mMove
    return bestMove

  def findBestMove(self, root):

    children = root.mChildren

    if len(children) > 0 and root.state == "unexplored":
      root.state =  "visited"
      for key in children:
        self.mMinMaxTree.insert(0,children[key])
      if len(self.mMinMaxTree) > 0:
        self.findBestMove(self.mMinMaxTree[0])
    elif len(children) > 0 and root.state == "visited":
      root.state = "explored"
      if root.depth % 2 == 0:
        getMax = True
      else:
        getMax = False
      root.mMaxScore = root.getMinMaxFromChildren(getMax)
      root.mMinScore = root.getMinMaxFromChildren(getMax)
      self.mMinMaxTree.pop(0)
      if len(self.mMinMaxTree) > 0:
        self.findBestMove(self.mMinMaxTree[0])
    else:
      root.state = "explored"
      if root.depth % 2 == 0:
        getMax = True
      else:
        getMax = False
      root.mMaxScore = root.getMinMaxFromChildren(getMax)
      root.mMinScore = root.getMinMaxFromChildren(getMax)
      self.mMinMaxTree.pop(0)
      if len(self.mMinMaxTree) > 0:
        self.findBestMove(self.mMinMaxTree[0])
      




  
