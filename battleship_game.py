import random

#step 1: Grid

def battelship_map (ship_position):
 """to make a 10 x 10 grid where the ships will be placed in"""

grid =[]           # empty list to store the rows and coloms

row_size = 10      # setting variable for row 
colom_size = 10    # setting variable to coloc

for row in range (row_size):     # 2 nested for loops to make the grid
    row = []                                    
    for _ in range (colom_size):
        
        row.append (".")
    grid.append(row)

for row in grid:
    print(" ".join(row))



#step 2 : User places their ships on the grid
# step 3 : Pc places its ships on the grid
# step 4 : select and check if the ship is destroyed
# step 5: play the game by taking turns
# make the ships bigger