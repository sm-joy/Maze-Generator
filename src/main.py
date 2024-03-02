import pygame
import CELL
from sys import exit

pygame.init()
pygame.display.set_caption("Maze Creator")

WINDOW_WIDTH, WINDOW_HEIGHT = 700, 700
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()

FPS = 300  # Control frames per second (since it's not a dynamic program, the FPS should be constant)
SLOW_MOTION_FPS = 10
CELL_WIDTH = 20
COLS, ROWS = int(WINDOW_WIDTH / CELL_WIDTH), int(WINDOW_HEIGHT / CELL_WIDTH)
START_ROW, START_COLUMN = 0, 0
END_ROW, END_COLUMN = ROWS-1, COLS-1


def main() -> int:
    """
    Main function to create a maze using depth-first search algorithm.

    Returns:
        int: Exit code (0 if successful, non-zero otherwise).
    """
    QUIT = False
    mazeCreated = False
    cells = [[CELL.Cell(row, col) for col in range(COLS)] for row in range(ROWS)]

#Variables for slow motion
    slowMotion = False

# Initialize the current cell to the starting cell
    currentCol, currentRow = START_COLUMN, START_ROW
    cellStack = []

# Main loop
    while not QUIT:
    # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QUIT = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    slowMotion = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    slowMotion = False

    # Update
        if not mazeCreated:
        # Mark the current cell as visited
            currentCell = cells[currentRow][currentCol]
            currentCell.visited = True

        # Get the next unvisited neighbor cell
            nextRow, nextCol = currentCell.checkNeighbors(pCells=cells, pRows=ROWS, pCols=COLS)
            nextCell = cells[nextRow][nextCol]

        # Check if there are unvisited cells
            if nextCol != -1 and nextRow != -1:
            # Push the cell if there are unvisited cells
                cellStack.append(currentCell)

            # Break walls while exploring the cells
                if currentRow - nextRow == -1:
                    currentCell.removeWall("bottom")
                    nextCell.removeWall("top")
                elif currentRow - nextRow == 1:
                    currentCell.removeWall("top")
                    nextCell.removeWall("bottom")
                elif currentCol - nextCol == -1:
                    currentCell.removeWall("right")
                    nextCell.removeWall("left")
                elif currentCol - nextCol == 1:
                    currentCell.removeWall("left")
                    nextCell.removeWall("right")

            # Mark the next cell as visited
                nextCell.visited = True
                currentRow, currentCol = nextRow, nextCol

            elif len(cellStack) > 0:
            # Backtrack if there are no unvisited cells
                popped_cell = cellStack.pop()
                currentCell = popped_cell
                currentCol, currentRow = popped_cell.col, popped_cell.row
            else:
                mazeCreated = True

    # Render

        for row in range(ROWS):
            for col in range(COLS):
                x = col * CELL_WIDTH
                y = row * CELL_WIDTH

            # Draw the visited cell
                if cells[row][col].visited:
                    cellRect = pygame.Rect(x, y, CELL_WIDTH, CELL_WIDTH)
                    pygame.draw.rect(surface=WINDOW, color="Purple", rect=cellRect)

            # Draw the walls of individual cells
                if cells[row][col].walls["top"]:
                    pygame.draw.line(surface=WINDOW, color="white", start_pos=(x, y), end_pos=(x + CELL_WIDTH, y))  # top
                if cells[row][col].walls["bottom"]:
                    pygame.draw.line(surface=WINDOW, color="white", start_pos=(x, y + CELL_WIDTH), end_pos=(x + CELL_WIDTH, y + CELL_WIDTH))  # bottom
                if cells[row][col].walls["left"]:
                    pygame.draw.line(surface=WINDOW, color="white", start_pos=(x, y), end_pos=(x, y + CELL_WIDTH))  # left
                if cells[row][col].walls["right"]:
                    pygame.draw.line(surface=WINDOW, color="white", start_pos=(x + CELL_WIDTH, y), end_pos=(x + CELL_WIDTH, y + CELL_WIDTH))  # right
        
    
        if mazeCreated:
            startCell_rect = pygame.Rect(START_COLUMN*CELL_WIDTH, START_ROW*CELL_WIDTH, CELL_WIDTH, CELL_WIDTH)
            pygame.draw.rect(surface=WINDOW, color="Green", rect=startCell_rect)

            endCell_rect = pygame.Rect(END_COLUMN*CELL_WIDTH, END_ROW*CELL_WIDTH, CELL_WIDTH, CELL_WIDTH)
            pygame.draw.rect(surface=WINDOW, color="Red", rect=endCell_rect)
        else:
        #Draw the current cell
            current_cellRect = pygame.Rect(currentCol * CELL_WIDTH, currentRow * CELL_WIDTH, CELL_WIDTH, CELL_WIDTH)
            pygame.draw.rect(surface=WINDOW, color="Blue", rect=current_cellRect)

    # Pygame update
        pygame.display.flip()
        if slowMotion:
            CLOCK.tick(SLOW_MOTION_FPS)
        else:
            CLOCK.tick(FPS)

# Pygame quit
    pygame.quit()
    exit()
    return 0


if __name__ == "__main__":
    exitCode = main()
    if not exitCode == 0:
        print("Something went wrong....")
