from random import randint
from BaseAI_3 import BaseAI
import time
import math

timeLimit = 0.19
availNums = [2, 4]

class PlayerAI(BaseAI):

    def __init__(self):
        self.startTime = time.clock()

    def getMove(self, grid):
        moves = grid.getAvailableMoves()
        move = self.maximize(grid)
        return moves[randint(0, len(moves) - 1)] if moves else None

    def maximize(self, grid):
        #if time is up, return 
        if (time.clock() - self.startTime) > timeLimit:
            return (None, self.getUtility(grid))
        (minChild, maxUtility) = (None, -math.inf)
        children = self.getMaxChildren(grid)
        for child in children:
            (_, utility) = self.minimize(child)
            if utility > maxUtility:
                (maxChild, maxUtility) = (child, utility)
        return (maxChild, maxUtility)


    def minimize(self, grid):
        #if time is up, return
        if (time.clock() - self.startTime) > timeLimit:
            return (None, self.getUtility(grid))
        (minChild, minUtility) = (None, math.inf)
        children = self.getMinChildren(grid)
        for child in children:
            (_, utility) = self.maximize(child)
            if utility < minUtility:
                (minChild, minUtility) = (child, utility)
        return (minChild, minUtility)

    def getMaxChildren(self, grid):
        children = []
        moves = grid.getAvailableMoves()
        for direction in moves:
            child = grid.clone()
            child.move(direction)
            children.append(child)
        return children

    def getMinChildren(self, grid):
        children = []
        cells = grid.getAvailableCells()
        for i, combo in enumerate(cells):
            j = 0
            while j < 2:
                child = grid.clone()
                child.setCellValue(combo, availNums[j])
                children.append(child)
                j = j + 1
        return children

    def getUtility(self, grid):
        return len(grid.getAvailableMoves()) + math.log(grid.getMaxTile()) + len(grid.getAvailableCells())

    

        

        