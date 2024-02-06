import random

column_letters = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "H": 7,
    "I": 8,
    "J": 9,
}    # making a dictionary to store the values of each letter

# step 1: Grid

def battleship_map ():
    """to make a 10 x 10 grid where the ships will be placed in"""

    print(" ", end=" ")   # printing a space before first letter, now first dot gets column A and row 0

    for letters in column_letters.keys():    # printing the alphabets to indicate the columns
        print(letters , end = " ")
    print()   

    grid =[]           # empty list to store the rows and coloms

    row_size = 10      # setting variable for row 
    column_size = 10    # setting variable to coloc


    for i in range (row_size):     # 2 nested for loops to make the grid
        row = []    
        print(i, end=" ")    # adding the numbers to indicate each row                       
        for j in range (column_size):
            row.append (".")
        grid.append(row)
        print(" ".join(row))    # print the row
    return grid
grid = battleship_map()


#step 2 : User places their ships on the grid

def users_ships_positions(grid):
    """ to ask the user for their ships position and check it the positions are valid. it returns the updated grid after the user has chosen the positions."""

    num_ships = 5    # limiting the number of ships to 5 

    for ship in range(num_ships):    # To ask the column and row for each ship separately 
        print("Where do you want ship ", ship + 1, "?")

        while True:    # as long as the condition is True ask for the user to enter the row position

            row = int(input("Choose a nummber from 0-9 for the row position of you ship:"))

            if 0 <= row <= 9:    # checking if the user entered a valid number for row 
                break
            else:
                print("Invalid row. Please choose a number from 0 to 9 for the row.")
                

        while True:    # as long as the condition is True, ask the user for the column alphabet 

            user_column = input("Choose a capital letter from A-J for the column position of your ship:").upper()

            if user_column in column_letters:    # getting the key value of each letter from dictionary and checking if its valid 

                column = column_letters[user_column]
                break 
            else:
                print("Invalid column. Please choose a capital letter from A to J.")

        grid[row][column] = "X"    # positioning the X in the users chosen columns and rows
    


users_grid = users_ships_positions(grid)

for row in users_grid:
    print(" ".join(row))

# step 3 : Pc places its ships on the grid
# step 4 : select and check if the ship is destroyed
# step 5: play the game by taking turns
# make the ships bigger
