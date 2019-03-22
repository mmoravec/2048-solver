from random import randint
from BaseAI_3 import BaseAI
from Grid_3 import Grid
import time
import math
import sys

timeLimit = 0.2
availNums = [2, 4]

class PlayerAI(BaseAI):

    def __init__(self):
        sys.setrecursionlimit(10000)

    def getMove(self, grid):
        self.startTime = time.clock()
        moves = grid.getAvailableMoves()
        grid.lastMove = 0
        move = self.maximize(grid, -math.inf, math.inf)
        if move[0] is not None and move[0].lastMove:
            return move[0].lastMove
        else:
            return 1

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
        sameTiles = {}
        samesies = 0
        for x in range(grid.size):
            for y in range(grid.size):
                sum = sum + grid.map[x][y]
                if grid.map[x][y] in sameTiles:
                    samesies = samesies + 1
                else:
                    sameTiles[grid.map[x][y]] = 1
        return  len(grid.getAvailableCells())