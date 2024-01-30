import random

# step 1: Grid

def battleship_map (ship_position):
    """to make a 10 x 10 grid where the ships will be placed in"""

    grid =[]           # empty list to store the rows and coloms

    row_size = 10      # setting variable for row 
    column_size = 10    # setting variable to coloc

    for i in range (row_size):     # 2 nested for loops to make the grid
        row = []                                    
        for j in range (column_size):
            row.append (".")
        grid.append(row)

    for position in ship_position:
        row, column = position
        grid[row][column] = "x"

    for row in grid:
        print(" ".join(row))

battleship_map([(0,0),(1,0),(2,2),(4,3),(8,9),(8,9)])
   



#step 2 : User places their ships on the grid
# step 3 : Pc places its ships on the grid
# step 4 : select and check if the ship is destroyed
# step 5: play the game by taking turns
# make the ships bigger