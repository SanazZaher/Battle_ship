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


    for ship in range(num_ships):      # To ask the column and row for each ship separately 
        print("Where do you want ship ", ship + 1, "?")

        while True:
            row = int(input("Choose a number from 0-9 for the row position of your ship:"))

            if 0 <= row <= 9:     # checking if the user entered a valid number for row 
                break
            else:
                print("Invalid row. Please choose a number from 0 to 9 for the row.")

        while True:
            user_column = input("Choose a letter from A-J for the column position of your ship:").upper()

            if user_column in column_letters:     # getting the key value of each letter from dictionary and checking if its valid 
                column = column_letters[user_column]
                break
            else:
                print("Invalid column. Please choose a capital letter from A to J.")

        grid[row][column] = "X"    # Placing the ship at the specified position on the grid.
    return grid

# printing the initial grid
grid = battleship_map()    
print("Initial Board:")
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

    for i in range(num_ships):    # Loop for each ship
        while True:
            row = random.randrange(0, 10)
            column = random.randrange(0, 10)

            if users_grid[row][column] != "X":    # Checking if the place has already been taken
                users_grid[row][column] = "X"
                break  # Break out of the inner loop once a ship is successfully placed

    return users_grid

computers_grid = computers_ships_positions(users_grid) 
print("Computer's Board:")
print_board(computers_grid)
