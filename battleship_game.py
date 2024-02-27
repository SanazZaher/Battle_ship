"""
Grid representation:
 "." = Empty cell (Water)
 "o" = Miss (Shot fired at this location, but it's empty/water)
 "X" = User Ship
 "P" = Computer Ship
 "#" = users Ship is completely sunk
 "~" = pc ship is completely sunk
 "H" = Part of the users ship is hit
 "C" = part of the pc ship is hit 
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
    ships = []   # list to store the ships
    ships_placed = 0 
    ship_info = [("Carrier", 5), ("Battleship", 4), ("Cruiser", 3), ("Submarine", 3), ("Destroyer", 2)]  # List of Cell lengths of the 5 ships and their names

    for ship_name, length in ship_info: 
        print(f"Where do you want {ship_name} (length:{length})?")
        
        # Row
        while True:
            try:    # checking input error
                row = int(input("Choose a number from 0-9 for the row position of your ship:"))
                if 0 <= row <= 9:     # checking if the user entered a valid number for row 
                    break
                else:
                    print("Invalid row. Please choose a number from 0 to 9 for the row.")
            except ValueError:
                print("Invalid input, enter a valid row number")
        # column
        while True:
            user_column = input("Choose a letter from A-J for the column position of your ship:").upper()

            if user_column in column_letters:     # getting the key value of each letter from dictionary and checking if its valid 
                column = column_letters[user_column]
                break
            else:
                print("Invalid column. Please choose a capital letter from A to J.")

        # orientation
        while True:       
            try:
                users_ships_orientation = input("Choose orientation (H for horizontal, V for vertical): ").upper()
                if users_ships_orientation == "H":
                    if column + length > 10:
                        raise ValueError("Invalid ship placement. Ship goes out of grid.")
                    positions = [(row,column + i ) for i in range (length)]   # making a list of positions
                    break
                elif users_ships_orientation == "V":
                    if row + length > 10:
                        raise ValueError("Invalid ship placement. Ship goes out of grid.")
                    positions = [(row + i, column) for i in range(length)]
                    break
                else:
                    print("Invalid orientation. Please choose H for horizontal or V for vertical.")
                    continue
            except ValueError as e:
                print(e)

        # add ships to the list
        ships.append({"name": ship_name, "length": length, "positions": positions, "hits": 0})

        # Mark the grid with the ship
        for position in positions:
            grid[position[0]][position[1]] = "X"

        ships_placed += 1    # to stop the questions after 5 ships are placed on the grid
        if ships_placed == num_ships:
            break
        print("\nCurrent Board:")
        print_board(grid)

    return grid, ships


# step 3: compute places ships randomly 

def computers_ships_positions(users_grid):
    """Places the computer's ships randomly on the user's grid."""

    num_ships = 5    # Limiting the number of ships for the computer
    pc_ships_placed = 0 
    pc_ships = []
    ship_info = [("Carrier", 5), ("Battleship", 4), ("Cruiser", 3), ("Submarine", 3), ("Destroyer", 2)]  # List of Cell lengths of the 5 ships and their names

    for ship_name, length in ship_info:
        while True:
            row = random.randrange(0, 10)
            column = random.randrange(0, 10)

            # orientation
            if users_grid[row][column] != "X":    # if the place is empty 
                pc_ships_orientation = random.choice(["H", "V"])    # random choice for orientation

                # situation Horizontal
                if pc_ships_orientation == "H":
                    if column + length <= 10:    # not to place it out of the grid 
                        positions = [(row,column + i) for i in range(length)]
                        break

                # situation vertical
                elif pc_ships_orientation == "V":
                    if row + length <= 10:
                        positions = [(row + i ,column) for i in range(length)]
                        break 
        # add ships to the list
        pc_ships.append({"name": ship_name, "length": length, "positions": positions, "hits": 0})
         # then mark the grids with pc ships
        for position in positions:
            if users_grid[position[0]][position[1]] != "X": # check the position
                users_grid[position[0]][position[1]] = "P"
    return users_grid, pc_ships

# step 4
def users_attack(users_grid, pc_ships):
    """Allows the user to guess the computer's ship positions and remove them from the grid."""
    bullet_num = 10

    for bullet in range(1, bullet_num + 1):  # Iterate over each bullet
        print(f"Let's attack! Where do you want to shoot your bullet {bullet} at? ")

        # Get user input for row
        while True:
            try:
                users_bullet_row = int(input("Choose a number from 0-9 for the row position of your shot: "))
                if 0 <= users_bullet_row <= 9:
                    break
                else:
                    print("Invalid row. Please choose a number from 0 to 9.")
            except ValueError:
                print("Invalid input. Please enter a valid row number.")

        # Get user input for column
        while True:
            column = input("Choose a letter from A-J for the column position of your shot: ").upper()
            if column in column_letters:
                users_bullet_column = column_letters[column]
                break
            else:
                print("Invalid column. Please choose a capital letter from A to J.")

        # Check the target of the shot
        target = users_grid[users_bullet_row][users_bullet_column]

        if target == "X":  # User hit their own ship
            print("You hit your own ship! That's a wasted shot.")
            print_board(users_grid)

        elif target == "P":  # User hit the computer's ship
            print("Hit! You hit part of a ship.")
            users_grid[users_bullet_row][users_bullet_column] = "H"  # Mark as hit
            print_board(users_grid)

            # Check if the ship is sunk
            for ship in pc_ships:
                if (users_bullet_row, users_bullet_column) in ship["positions"]:
                    ship["hits"] += 1
                    if ship["hits"] == ship["length"]:
                        print(f"You've sunk {ship['name']}!")
                        # Mark the ship as sunk on the grid
                        for position in ship["positions"]:
                            users_grid[position[0]][position[1]] = "#" if users_grid[position[0]][position[1]] !="H" else "H" # Mark as sunk
                        pc_ships.remove(ship)  # Remove the ship from the list
                        print_board(users_grid)
                        
                        # Check if all ships are sunk
                        if not pc_ships:
                            print("Congratulations! You've sunk all the computer's ships!")
                        break   
            else:  # User missed
                print("Miss! You hit the water.")
                users_grid[users_bullet_row][users_bullet_column] = "o"  # Mark as a miss on water
                
            
        print_board(users_grid)  # Print the updated grid after each shot
    
    # If all bullets are fired and all ships are not sunk, the game is over
    print("You've used all your bullets. Game over.")
    return users_grid, False

# step 5
def computers_attack(users_grid, users_ships):
    """pc hits the bullets randomly and gives the board updated"""

    bullet_num = 10
    for bullet in range(1, bullet_num + 1):
        print(f"Computer's turn to attack (bullet {bullet}): ")

        while True:
            computers_bullet_row = random.randit(0,9)
            computers_bullet_column = random.randit(0,9)
            break
    target = users_grid[computers_bullet_row][computers_bullet_column]

    if target == "X":  # if the bullet hits the users ship
        print("Hit! Computer hit part of your ship.")
        users_grid[computers_bullet_row][computers_bullet_column c] = "H"  # Mark as hit
        print_board(users_grid)

    elif target == "o":
        print("computer hit the water. ")
        users_grid[computers_bullet_row][computers_bullet_column] = "o"  # Mark as hit
        print_board(users_grid)

        for ship in users_ships:
                if (computers_bullet_row, computers_bullet_column) in ship["positions"]:
                    ship["hits"] += 1
                    if ship["hits"] == ship["length"]:
                        print(f"Computer sunk your {ship['name']}!")

                        # Mark the ship as sunk on the grid
                        for position in ship["positions"]:
                            users_grid[position[0]][position[1]] = "~" if users_grid[position[0]][position[1]] !="H" else "H" # Mark as sunk
                        users_ships.remove(ship)  # Remove the ship from the list
                        print_board(users_grid)
                        # Check if all user ships are sunk
                        if not users_ships:
                            print("Game Over. Computer sunk all your ships!")
                        break
                    else:  # Computer missed
                        print("Miss! Computer hit the water.")
                        users_grid[computers_bullet_row][computers_bullet_column] = "o"  # Mark as a miss on water
                        print_board(users_grid)
                else:  # Computer missed
                    print("Miss! Computer hit the water.")
                    users_grid[computers_bullet_row][computers_bullet_column] = "o"  # Mark as a miss on water
                    print_board(users_grid)
        

def main():
    # Printing the initial grid
    grid = battleship_map()
    print("\nInitial Board:")
    print_board(grid)

    # User places the ships
    users_grid, user_ships = users_ships_positions(grid)
    print("User's Board:")
    print_board(users_grid)

    # Computer places the ships
    users_grid, computer_ships = computers_ships_positions(users_grid)
    print("Computer's Board:")
    print_board(users_grid)

    # User attacks computer's ships
    users_grid, game_over = users_attack(users_grid, computer_ships)

    if game_over:
        print("Game Over")

if __name__ == "__main__":
    main()

    
