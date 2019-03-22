from random import randint
from BaseAI_3 import BaseAI
from Grid_3 import Grid
import time
import math

timeLimit = 0.4
availNums = [2, 4]

class PlayerAI(BaseAI):

    def __init__(self):
        self.startTime = time.clock()

    def getMove(self, grid):
        self.startTime = time.clock()
        moves = grid.getAvailableMoves()
        grid.lastMove = None
        move = self.maximize(grid, -math.inf, math.inf)
        return move[0].lastMove

    def maximize(self, grid, alpha, beta):
        #if time is up, return 
        if (time.clock() - self.startTime) > timeLimit:
            return (grid, self.getUtility(grid))
        (maxChild, maxUtility) = (None, -math.inf)
        children = self.getMaxChildren(grid)
        for child in children:
            (_, utility) = self.minimize(child, alpha, beta)
            if utility > maxUtility:
                (maxChild, maxUtility) = (child, utility)
            if maxUtility >= beta:
                break
            if maxUtility > alpha:
                alpha = maxUtility
        return (maxChild, maxUtility)


    def minimize(self, grid, alpha, beta):
        #if time is up, return
        if (time.clock() - self.startTime) > timeLimit:
            return (grid, self.getUtility(grid))
        (minChild, minUtility) = (None, math.inf)
        children = self.getMinChildren(grid)
        for child in children:
            (_, utility) = self.maximize(child, alpha, beta)
            if utility < minUtility:
                (minChild, minUtility) = (child, utility)
            if minUtility <= alpha:
                break
            if minUtility < beta:
                beta = minUtility
        return (minChild, minUtility)

    def getMaxChildren(self, grid):
        children = []
        moves = grid.getAvailableMoves()
        for direction in moves:
            child = grid.clone()
            child.move(direction)
            child.lastMove = direction
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
        sum = 0
        twosAndFours = 0
        for x in range(grid.size):
            for y in range(grid.size):
                if grid.map[x][y] is 2 or grid.map[x][y] is 4:
                    twosAndFours = twosAndFours + 1
                sum = sum + grid.map[x][y]
        return  len(grid.getAvailableCells()) + math.log2(sum / (grid.size*grid.size)) - twosAndFours