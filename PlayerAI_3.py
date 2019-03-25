from random import randint
from BaseAI_3 import BaseAI
from Grid_3 import Grid
import time
import math
import sys
import statistics

timeLimit = 0.2
availNums = [2, 4]
directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))

class PlayerAI(BaseAI):

    def __init__(self, weights):
        sys.setrecursionlimit(10000)
        self.weights = weights

    def getMove(self, grid):
        self.startTime = time.clock()
        moves = grid.getAvailableMoves()
        grid.lastMove = 0
        move = self.maximize(grid, -math.inf, math.inf)
        if move[0] is not None and move[0].lastMove:
            return move[0].lastMove
        else:
            return moves[randint(0, len(moves) - 1)] if moves else None

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

    def sameNumbers(self, grid):
        nums = {}
        total = 0
        for x in range(grid.size):
            for y in range(grid.size):
                if grid.map[x][y] in nums and grid.map[x][y] is not 0:
                    if grid.map[x][y] > 4:
                        total = total + 1
                else:
                    nums[grid.map[x][y]] = 1
        return total

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
        emptyWeight, monoWeight, maxWeight, sameWeight, smoothWeight  = 1, 1, 0.005, -0.5, -0.001
        smoothVal = self.smoothness(grid) * smoothWeight
        emptyVal = len(grid.getAvailableCells()) * emptyWeight
        maxVal = grid.getMaxTile() * maxWeight
        return  emptyVal + smoothVal + maxVal

    def monotonicity(self, grid):
        totals = [0, 0, 0, 0]
        for x in range(4):
            current = 0
            next = current + 1
            while next < 4:
                while next < 4 and grid.map[x][next] != 0:
                    next = next + 1
                if next >= 4:
                    next = next -1
                currentValue = 0 if grid.map[x][current] is 0 else math.log(grid.map[x][current] / math.log(2))
                nextValue = 0 if grid.map[x][next] is 0 else math.log(grid.map[x][next] / math.log(2))
                if currentValue > nextValue:
                    totals[0] = totals[0] + nextValue - currentValue
                elif nextValue > currentValue:
                    totals[1] = totals[1] + currentValue - nextValue
                current = next
                next = next + 1
        
        for y in range(4):
            current = 0
            next = current + 1
            while next < 4:
                while next < 4 and grid.map[next][y] != 0:
                    next = next + 1
                if next >= 4:
                    next = next -1
                currentValue = 0 if grid.map[current][y] is 0 else math.log(grid.map[current][y] / math.log(2))
                nextValue = 0 if grid.map[next][y] is 0 else math.log(grid.map[next][y] / math.log(2))
                if currentValue > nextValue:
                    totals[2] = totals[2] + nextValue - currentValue
                elif nextValue > currentValue:
                    totals[3] = totals[3] + currentValue - nextValue
                current = next
                next = next + 1

        return max(totals[0], totals[1]) + max(totals[2], totals[3])

    def medianNumbers(self, grid):
        median = []
        for x in range(grid.size):
            for y in range(grid.size):
                median.append(grid.map[x][y])
        return statistics.median(median)

    def bottomRowNumbers(self, grid):
        total = 0
        for x in range(2,4):
            for y in range(grid.size):
                if grid.map[x][y] is 2 or grid.map[x][y] is 4:
                    total = total + 1
        return total
    
    def smoothness(self, grid):
        smooth = 0
        for x in range(grid.size):
            for y in range(grid.size):
                cell = grid.map[x][y]
                if y - 1 > 0:
                    if abs(grid.map[x][y-1] - cell) is 0 and cell > 16:
                        smooth = smooth - 3 * cell
                    else:
                        smooth = abs(grid.map[x][y-1] - cell) + smooth
                if y + 1 < 4:
                    if abs(grid.map[x][y+1] - cell) is 0 and cell > 16:
                        smooth = smooth - 3 * cell
                    else:
                        smooth = abs(grid.map[x][y+1] - cell) + smooth
                if x - 1 > 0:
                    if abs(grid.map[x-1][y] - cell) is 0 and cell > 16:
                        smooth = smooth - 3 * cell
                    else:
                        smooth = abs(grid.map[x-1][y] - cell) + smooth
                if x + 1 < 4:
                    if abs(grid.map[x+1][y] - cell) is 0 and cell > 16:
                        smooth = smooth - 3 * cell
                    else:
                        smooth = abs(grid.map[x+1][y] - cell) + smooth
        return smooth if smooth != 0 else 1