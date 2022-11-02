import pygame
import sys
import random

def main():
    pygame.init()

    width, height = 800, 500
    display = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Game of life")
    clock = pygame.time.Clock()

    display.fill((255, 255, 255))
    gameGrid = GameGrid((0, 0), (width, height), 8, display)
    #gameGrid.printGrid()
    paused = True
    clicked = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                clicked = pygame.mouse.get_pos()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    paused = not paused

                if event.key == pygame.K_ESCAPE:
                    gameGrid.clear()

                if event.key == pygame.K_RETURN:
                    running = False
                    
        if clicked is not None:
            gameGrid.toggleLife(*pygame.mouse.get_pos())
            clicked = None

        if not paused:
            gameGrid.update()
        gameGrid.render()
        
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
    sys.exit(0)


class GameGrid:

    def __init__(self, xy, wh, cellSize, display):
        self.x, self.y = xy
        self.width, self.height = wh
        self.cellSize = cellSize
        self.grid = [[Cell(x, y, cellSize, display) for x in range(self.x, self.x+self.width, cellSize)]
                     for y in range(self.y, self.y+self.height, cellSize)]
        self._createGrid()

    def _createGrid(self, infinite=True):
        for x in range(0, len(self.grid)):
            for y in range(0, len(self.grid[0])):
                self.grid[x][y]._link(*self._getNeighbors(x, y))
    
    def _getNeighbors(self, x, y):
        if y == 0: up = len(self.grid[0]) -1
        else: up = y - 1

        if y == len(self.grid[0]) -1: down = 0
        else: down = y + 1

        if x == 0: left = len(self.grid) -1
        else: left = x - 1

        if x == len(self.grid) -1: right = 0
        else: right = x + 1

        return self.grid[x][up], self.grid[right][up],\
               self.grid[right][y], self.grid[right][down],\
               self.grid[x][down], self.grid[left][down],\
               self.grid[left][y], self.grid[left][up]

    def update(self):
        for column in self.grid:
            for cell in column:
                cell.update(True)

        for column in self.grid:
            for cell in column:
                cell.update(False)

    def render(self):
        for column in self.grid:
            for cell in column:
                cell.draw()

    def toggleLife(self, x, y):
        for column in self.grid:
            for cell in column:
                if cell.rect.collidepoint(x, y):
                    cell.toggleLife()
                    cell.draw()

    def clear(self):
        for column in self.grid:
            for cell in column:
                cell.clear()

    def printGrid(self):
        for row in self.grid:
            print("[", end="")
            for cell in row:
                if row.index(cell) == len(row)-1:
                    print(str(cell.alive) + "]")
                    break
                print(str(cell.neighbors[0].y) + ",", end="")
            

class Cell:

    def __init__(self, x, y, cellSize, display):
        self.x, self.y = x, y
        self.cellWidth = cellSize
        self.display = display
        self.neighbors = [] #N, NE, E, SE, S, SW, W, NW
        self.alive = False
        self.newState = False
        self.colour = 0, 200, 0
        self.newColour = 0, 200, 0
        self.rect = pygame.Rect(x, y, cellSize, cellSize)

    def _link(self, n, ne, e, se, s, sw, w, nw):
        self.neighbors = [n, ne, e, se, s, sw, w, nw]

    def update(self, first):
        if first:
            numAlive = 0
            for i in self.neighbors:
                numAlive += int(i.alive)

            if self.alive:
                if numAlive < 2 or numAlive > 3:
                    self.newState = False
                elif numAlive == 2 or numAlive == 3:
                    self.newState = True
            else:
                if numAlive == 3:
                    self.newState = True
        else:
            self.alive = self.newState
            self.colour = self.newColour

    def clear(self):
        self.alive = False
        self.newState = False

    def draw(self):
        colour = int(self.alive) * self.colour[0], int(self.alive) * self.colour[1], \
                 int(self.alive) * self.colour[2]
        pygame.draw.rect(self.display, colour, self.rect)

    def toggleLife(self):
        self.alive = not self.alive
        

if __name__ == '__main__':
    main()
