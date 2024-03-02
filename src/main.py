import pygame as pg
import CELL
from sys import exit
import os

parentDir = os.path.dirname(__file__)[0 : len(os.path.dirname(__file__))-4]

pg.init()
pg.display.set_caption("Maze Creator")
pg.display.set_icon(pg.image.load(os.path.join(parentDir, "res", "icon.png")))

WINDOW_WIDTH, WINDOW_HEIGHT = 700, 700
WINDOW = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pg.time.Clock()

FPS = 120  # Control frames per second (since it's not a dynamic program, the FPS should be constant)
SLOW_MOTION_FPS = 10
CELL_WIDTH = 70
COLS, ROWS = int(WINDOW_WIDTH / CELL_WIDTH), int(WINDOW_HEIGHT / CELL_WIDTH)
START_ROW, START_COLUMN = 0, 0
END_ROW, END_COLUMN = ROWS-1, COLS-1



def saveFrame() -> None:
    pg.image.save(WINDOW, os.path.join(parentDir, "res", "maze_images", f"maze.png"))
    print("Image Saved Successfully")


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
        for event in pg.event.get():
            if event.type == pg.QUIT:
                QUIT = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    slowMotion = True
                elif (event.key == pg.K_s) and (pg.key.get_mods() & pg.KMOD_CTRL) and mazeCreated:
                    saveFrame()
            elif event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
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
        WINDOW.fill("#F5F5F5") #Background Color
        for row in range(ROWS):
            for col in range(COLS):
                x = col * CELL_WIDTH
                y = row * CELL_WIDTH

            # Draw the visited cell
                if cells[row][col].visited:
                    cellRect = pg.Rect(x, y, CELL_WIDTH, CELL_WIDTH)
                    pg.draw.rect(surface=WINDOW, color="#FFC0CB" if not mazeCreated else "Purple", rect=cellRect)

            # Draw the walls of individual cells
                if cells[row][col].walls["top"]:
                    pg.draw.line(surface=WINDOW, color="#001F3F" if not mazeCreated else "White", start_pos=(x, y), end_pos=(x + CELL_WIDTH, y))  # top
                if cells[row][col].walls["bottom"]:
                    pg.draw.line(surface=WINDOW, color="#001F3F" if not mazeCreated else "White", start_pos=(x, y + CELL_WIDTH), end_pos=(x + CELL_WIDTH, y + CELL_WIDTH))  # bottom
                if cells[row][col].walls["left"]:
                    pg.draw.line(surface=WINDOW, color="#001F3F" if not mazeCreated else "White", start_pos=(x, y), end_pos=(x, y + CELL_WIDTH))  # left
                if cells[row][col].walls["right"]:
                    pg.draw.line(surface=WINDOW, color="#001F3F" if not mazeCreated else "White", start_pos=(x + CELL_WIDTH, y), end_pos=(x + CELL_WIDTH, y + CELL_WIDTH))  # right
        
    
        if mazeCreated:
            startCell_rect = pg.Rect(START_COLUMN*CELL_WIDTH, START_ROW*CELL_WIDTH, CELL_WIDTH, CELL_WIDTH)
            pg.draw.rect(surface=WINDOW, color="#006400", rect=startCell_rect)

            endCell_rect = pg.Rect(END_COLUMN*CELL_WIDTH, END_ROW*CELL_WIDTH, CELL_WIDTH, CELL_WIDTH)
            pg.draw.rect(surface=WINDOW, color="#8B0000", rect=endCell_rect)
        else:
        #Draw the current cell
            current_cellRect = pg.Rect(currentCol * CELL_WIDTH, currentRow * CELL_WIDTH, CELL_WIDTH, CELL_WIDTH)
            pg.draw.rect(surface=WINDOW, color="#008080", rect=current_cellRect)

    # Pygame update
        pg.display.flip()
        if slowMotion:
            CLOCK.tick(SLOW_MOTION_FPS)
        else:
            CLOCK.tick(FPS)

# Pygame quit
    pg.quit()
    exit()
    return 0


if __name__ == "__main__":
    exitCode = main()
    if not exitCode == 0:
        print("Something went wrong....")
