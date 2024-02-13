"""
Grid representation:
 "." = Empty cell (Water)
 "o" = Miss (Shot fired at this location, but it's empty/water)
 "X" = User Ship
 "P" = Computer Ship
 "#" = Ship is completely sunk
 "H" = Part of the ship is hit
"""
import random
# making a dictionary to store the values of each letter
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
}  
 # step 1: Grid

def print_board(grid):
    """Prints the board with row numbers, column letters, and ships marked with 'X'."""
    
    print(" ", end=" ")    # printing the column letters
    for letter in column_letters.keys():  
        print(letter, end=" ")
    print()

    for i in range(len(grid)):    # printing each row with numbers
        print(i, end=" ")  
        for j in range(len(grid[i])):
            print(grid[i][j], end=" ")
        print()

def battleship_map():
    """Generates a 10x10 grid for the battleship game."""
    grid = []
    for i in range(10):   # looping through each row
        row = []
        for j in range(10):    # looping through each column
            row.append(".")
        grid.append(row)
    return grid

#step 2 : User places their ships on the grid

def users_ships_positions(grid):
    """Allows the user to place their ships on the grid."""
    num_ships = 5     # limiting the number of ships to 5 
    ships_placed = 0 
    ship_lengths = [3, 4, 2, 5, 3]  # List of Cell lengths of the 5 ships

    for i in range(len(ship_lengths)): 
        ship = i +1    # ship number starting from 1
        length = ship_lengths[i]
        
        # To ask the column and row for each ship separately 
        print(f"Where do you want ship ", ship,"?")

        while True:
            try:    # checking input error
                row = int(input("Choose a number from 0-9 for the row position of your ship:"))

                if 0 <= row <= 9:     # checking if the user entered a valid number for row 
                    break
                else:
                    print("Invalid row. Please choose a number from 0 to 9 for the row.")
            except ValueError:
                print("Invalid input, enter a valid row number")

        while True:
            user_column = input("Choose a letter from A-J for the column position of your ship:").upper()

            if user_column in column_letters:     # getting the key value of each letter from dictionary and checking if its valid 
                column = column_letters[user_column]
                break
            else:
                print("Invalid column. Please choose a capital letter from A to J.")

        while True:       
            try:
                users_ships_orientation = input("Choose orientation (H for horizontal, V for vertical): ").upper()
                if users_ships_orientation == "H":
                    if column + length > 10:
                        raise ValueError("Invalid ship placement. Ship goes out of grid.")
                    for i in range(length):
                        grid[row][column + i] = "X"
                    break
                elif users_ships_orientation == "V":
                    if row + length > 10:
                        raise ValueError("Invalid ship placement. Ship goes out of grid.")
                    for i in range(length):
                        grid[row + i][column] = "X"
                    break
                else:
                    print("Invalid orientation. Please choose H for horizontal or V for vertical.")
                continue
            except ValueError as e:
                print(e)
            
        ships_placed += 1    # to stop the questions after 5 ships are placed on the grid
        if ships_placed == num_ships:
            break
        
        print("\nCurrent Board:")
        print_board(grid)   # Printing the current board after placing each ship
    return grid

# printing the initial grid
grid = battleship_map()    
print("\nInitial Board:")
print_board(grid)

# user places the ships
users_grid = users_ships_positions(grid)

# printing the grid after ships placed
print("User's Board:")
print_board(users_grid)

# step 3: compute places ships randomly 

def computers_ships_positions(users_grid):
    """Places the computer's ships randomly on the user's grid."""

    num_ships = 5    # Limiting the number of ships for the computer
    pc_ships_placed = 0 
    ship_lengths = [3, 4, 2, 5, 3]  # List of Cell lengths of the 5 ships
    for i in range(len(ship_lengths)):    # Loop for each ship
        ships = i + 1
        length = ship_lengths [i]

        while True:
            row = random.randrange(0, 10)
            column = random.randrange(0, 10)

            # orientation
            if users_grid[row][column] != "X":    # if the place is empty 
                pc_ships_orientation = random.choice(["H", "V"])    # random choice for orientation

                # situation Horizontal
                if pc_ships_orientation == "H":
                    if column + length <= 10:    # not to place it out of the grid 
                        for j in range(length):
                            if users_grid[row][column + j] != "X":    # check if the place is not been marked by user
                                users_grid[row][column + j] = "P"
                            else:
                                break
                        else:
                            pc_ships_placed += 1 # then add the next ship
                            break

                # situation vertical
                elif pc_ships_orientation == "V":
                    if row + length <= 10:
                        for j in range(length):
                            if users_grid[row + j][column] != "X":
                               users_grid[row+ j][column] = "P"
                            else:
                               break 
                        else:
                            pc_ships_placed += 1 
                            break
    return users_grid

computers_grid = computers_ships_positions(users_grid) 
print("Computer's Board:")
print_board(computers_grid)
