import random   # Use for randomise values in the matrix
import copy     # Use for copy the matrix while updating
import pygame   # Use for UI
from pygame.locals import (K_ESCAPE, KEYDOWN, QUIT)


"""""""""""""""" """"""""""'"""""""
"""            UI               """
"""""""""""""""" """"""""""'"""""""
pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH: int = 600
SCREEN_HEIGHT = 620
font = pygame.font.SysFont("Lato", 70)

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.get_surface().fill((255, 255, 255))  # background

def createSquare(x, y, color):
    pygame.draw.rect(screen, color, [x, y, 15, 15 ])

def visualizeGrid(matrix, N):
    y = SCREEN_HEIGHT/2 - (N * 6)  # we start at the top of the screen
    for row in matrix:
        x = SCREEN_WIDTH/2 - (N * 7.5) # for every row we start at the left of the screen again
        for item in row:
            if item == 0:
                createSquare(x, y, (255, 255, 255))
            else:
                createSquare(x, y, (0, 0, 0))

            x += 15 # for ever item/number in that row we move one "step" to the right
        y += 15   # for every new row we move one "step" downwards


def write(text, x, y, color="Cornflower blue",):
    "returns a text on a surface with the position in a rect"
    text = font.render(text, 1, pygame.Color(color))
    text_rect = text.get_rect(center=(SCREEN_WIDTH/2, y))

    return text, text_rect

"""""""""""""""" """"""""""'"""""""
"""           UI ends           """
"""""""""""""""" """"""""""'"""""""


def createMatrix(rowCount, colCount, data):
    '''
    :param rowCount: Row dimension
    :param colCount: colomn dimension
    :param data: matrix input data
    :return: matrix with values that indicates which cell is alive.
    '''

    newMatrix = []
    for i in range(rowCount):
        rowList = []
        for j in range(colCount):
            # you need to increment through dataList here, like this:
            rowList.append(data[rowCount * i + j])
        newMatrix.append(rowList)

    return newMatrix


def createRandomMatrix(N):
    '''
    Use once to initialize the game.
    0 - dead cell.
    1 - live cell.
    :param N: Matrix dimension, and use for N*N Number of random choices.
    :return : Matrix with random values.
    '''

    dataLis = [0,1]
    randomLis = random.choices(dataLis, weights=[1,3], k=N*N)
    randomMatrix = createMatrix(N, N, randomLis)
    return randomMatrix


def updateMatrix(N,adjacencyMatrix):
    '''
    Each iteration the matrix is updated by conditions, which depends on every cell's neighbors.
    :param N: Matrix dimension
    :param adjacencyMatrix: Current matrix
    :return: Updated matrix
    '''

    newAdjacencyMat = copy.deepcopy(adjacencyMatrix)

    for i in range(N):
        for j in range(N):
            # count the live neighbours
            num_live_neighbors = 0
            # use modulo operator to make the values wrap around at the edge
            coordinateList = [[i,(j - 1) % N], [i,(j + 1) % N], [(i - 1) % N,j], [(i + 1) % N,j],
                              [(i - 1) % N,(j - 1) % N], [(i - 1) % N, (j + 1) % N],
                              [(i + 1) % N, (j - 1) % N], [(i + 1) % N,(j + 1) % N]]

            for element in coordinateList:
                # calculate neighbors that in the range and live.
                if abs(element[0] - i) <= 1 and abs(element[1] - j) <= 1:
                    if adjacencyMatrix[element[0]][element[1]] == 1:
                        num_live_neighbors += 1
            # conditions for the new status of the cell
            if adjacencyMatrix[i][j] == 1:
                if (num_live_neighbors < 2) or (num_live_neighbors > 3):
                    newAdjacencyMat[i][j] = 0
            else:
                if num_live_neighbors == 3:
                    newAdjacencyMat[i][j] = 1
    return newAdjacencyMat


def main():
    '''
    matrix neighbors' cells
             |       |
    (i-1,j-1)|(i-1,j)|(i-1,j+1)
    ---------|-------|----------
     (i,j-1) | (i,j) | (i,j+1)
    ---------|-------|----------
    (i+1,j-1)|(i+1,j)|(i+1,j+1)
             |       |
    '''

    """"""""""""""""""""""""""""""""""""""""""""
    """" remove the seed for randomization """""
    """"""""""""""""""""""""""""""""""""""""""""
    random.seed(3)    # Use for the same random simulation each time.
    game_dataSet = []     # list of matrices of each iteration use later in the UI section
    N = 30      # Matrix dimension

    gameMatrix = createRandomMatrix(N)     # create a random world
    newGameMatrix = updateMatrix(N, gameMatrix)

    game_dataSet.append(gameMatrix)
    game_dataSet.append(newGameMatrix)

    # Continues iterations while the matrix is updating
    while gameMatrix != newGameMatrix:
        gameMatrix = newGameMatrix
        newGameMatrix = updateMatrix(N,gameMatrix)
        game_dataSet.append(newGameMatrix)


    # UI implementaion
    running = True
    clock = pygame.time.Clock()
    text, text_rect = write("Conway's Game Of Life", 10, 70)

    # Main loop
    while running:
        for iter in game_dataSet:
            # Did the user close the program? stop immediately.
            if running == False:
                break

            screen.blit(text, text_rect)
            pygame.display.update()
            visualizeGrid(iter, N)  # call the function
            clock.tick(2)

            # Look at every event in the queue
            for event in pygame.event.get():
                # Did the user hit a key?
                if event.type == KEYDOWN:
                    # Was it the Escape key? If so, stop the loop.
                    if event.key == K_ESCAPE:
                        running = False

                # Did the user click the window close button? If so, stop the loop.
                elif event.type == QUIT:
                    running = False


if __name__ == '__main__':
    main()