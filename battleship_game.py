"""
Grid representation:
 "." = Empty cell (Water)
 "O" = Miss (Shot fired at this location, but it's empty/water)
 "X" = User Ship
 "P" = Computer Ship
 "#" = Ship is completely sunk
 "H" = Part of theship is hit
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

def users_ships_positions(users_grid):
    """Allows the user to place their ships on the grid."""
    num_ships = 5     # limiting the number of ships to 5 
    ships = []   # list to store the ships
    ships_placed = 0 
    ship_info = [("Carrier", 5), ("Battleship", 4), ("Cruiser", 3), ("Submarine", 3), ("Destroyer", 2)]  # List of tupples with Cell lengths of the 5 ships and their names

    for ship_name, length in ship_info: # tupple unpacking
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

        # Check for overlap
        overlap_detected = any(users_grid[position[0]][position[1]] == "X" for position in positions)

        if overlap_detected:
            print("You overlapped with another ship! Please choose a new placement for your ship.")
            continue

        # Check for adjacency
        adjacency_detected = False
        for position in positions:
            row, col = position
            for i in range(-1, length + 1):
                for j in range(-1, 2):
                    if 0 <= row + i < 10 and 0 <= col + j < 10:
                        if users_grid[row + i][col + j] == "X":
                            adjacency_detected = True
                            break
                if adjacency_detected:
                    break
            if adjacency_detected:
                break

        if adjacency_detected:
            print("Invalid position! Ships cannot be placed adjacent to each other.")
            print("Please choose a new placement for your ship.")
            continue

        # No overlap or adjacency, add the ship to the list and mark its positions on the grid
        ships.append({"name": ship_name, "length": length, "positions": positions, "hits": 0})
        for position in positions:
            users_grid[position[0]][position[1]] = "X"
        print("\nCurrent Board:")
        print_board(users_grid)

    print("All your ships have been placed.")
    return users_grid, ships

# step 3: compute places ships randomly 
def computers_ships_positions(pc_grid, debug_mode = True):  
    """Places the computer's ships randomly on the separate grid and this wont be revealed to the user."""   # adding the debug mode for the pc ships to not display them on the board

    num_ships = 5    # Limiting the number of ships for the computer
    pc_ships_placed = 0 
    pc_ships = []
    ship_info = [("Carrier", 5), ("Battleship", 4), ("Cruiser", 3), ("Submarine", 3), ("Destroyer", 2)]  # List of Cell lengths of the 5 ships and their names

    for ship_name, length in ship_info:   # iterating over each ship to place them on the grid
        placed = False   # to check if the ship is placed successfully
        while not placed:
            row = random.randrange(0, 10)
            column = random.randrange(0, 10)
            pc_ships_orientation = random.choice(["H", "V"])    # random choice for orientation
        
            # situation Horizontal
            if pc_ships_orientation == "H":
                if column + length <= 10:    # not to place it out of the grid 
                    positions = [(row,column + i) for i in range(length)]
                    placed = True   # pc places the ship horizontally 
            # situation vertical
            elif pc_ships_orientation == "V":
                if row + length <= 10:
                    positions = [(row + i ,column) for i in range(length)]
                    placed = True   # pc can place the ship vertically
            if placed:
                # check for overlap with users ships, if any of this is true  
                overlap = any(pc_grid[position[0]][position[1]] == "X" for position in positions)
                if not overlap:   # if there is no overlap                 
                    # add ships to the list
                    pc_ships.append({"name": ship_name, "length": length, "positions": positions, "hits": 0})

                    # then mark the grids with pc ships
                    for position in positions:
                        pc_grid[position[0]][position[1]] = "P"
                    pc_ships_placed += 1
                else:
                    placed = False 

                # Check ships cells for overlap, ships can't be placed next to each other
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if (position[0] + i >= 0 and position[0] + i < 10) and (position[1] + j >= 0 and position[1] + j < 10):
                            if pc_grid[position[0] + i][position[1] + j] == "X":
                                overlap = True
                                break  
    if debug_mode:
        print("\nComputer's ships:")
        print_board(pc_grid)  # Printing computer's ships for debugging

    return pc_grid, pc_ships

def print_board(grid, reveal= True):
    """Prints the board with row numbers, column letters, and ships marked with 'X'."""
    print(" ", end=" ")    # Printing the column letters
    for letter in column_letters.keys():  
        print(letter, end=" ")
    print()

    for i in range(len(grid)):    # Printing each row with numbers
        print(i, end=" ")  
        for j in range(len(grid[i])):
            if not reveal and grid[i][j] == "P":  # If not reveal mode and grid cell has a PC ship, print "." instead
                print(".", end=" ")
            else:
                print(grid[i][j], end=" ")
        print()

# step 4
def users_attack(pc_grid, pc_ships):
    """Allows the user to guess the computer's ship positions and remove them from the grid."""
    bullet_num = 20
    bullet_used = 0   # for the condition game over when all the bullets are fired
    for bullet in range(1, bullet_num + 1):  # Iterate over each bullet
        print(f"\nLet's attack! Where do you want to shoot your bullet {bullet} at? ")

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
        target = pc_grid[users_bullet_row][users_bullet_column]

        if target == "P":  # User hit the computer's ship
            print("\nHit! You hit part of a ship.")
            pc_grid[users_bullet_row][users_bullet_column] = "H"  # Mark as hit
            print_board(pc_grid)

            # Check if the ship is sunk
            for ship in pc_ships:
                if (users_bullet_row, users_bullet_column) in ship["positions"]:
                    ship["hits"] += 1
                    if ship["hits"] == ship["length"]:
                        print(f"You've sunk {ship['name']}!")
                        # Mark the ship as sunk on the grid
                        for position in ship["positions"]:
                            pc_grid[position[0]][position[1]] = "#" # Mark as sunk
                        print_board(pc_grid)
                        pc_ships.remove(ship)  # Remove the ship from the list
                        print("Remaining ships:", pc_ships)   # for debugging the sunk condition 
                        print("All ships sunk?", all(ship["hits"] == ship["length"] for ship in pc_ships))

                        # Check if all ships are sunk(If all the conditions are true, return true)
                        if all(ship["hits"] == ship["length"] for ship in pc_ships):
                            print("Congratulations! You've sunk all the computer's ships!")
                            return pc_grid, True   # game over situation is if all the ships are sunk or if all the bullets are fired
                        elif bullet_used == bullet_num:
                            print("You've used all your bullets.Game over!")
                            return pc_grid, False
                        break   
        else:  # User missed and hit the water
            print("Miss! You hit the water.")
            pc_grid[users_bullet_row][users_bullet_column] = "O"  # Mark as a miss on water 
            print_board(pc_grid)  # Print the updated grid after each shot 
        bullet_used += 1   #increment the bulloet used      
    
    
    # If all bullets are fired and all ships are not sunk, the game is over
    print("You've used all your bullets. Game over.")
    return pc_grid, False


# step 5
def computers_attack(users_grid, users_ships):
    """Computer attacks the user's grid randomly and gives the updated board."""
    bullet_num = 20
    bullet_used = 0 
    for bullet in range(1, bullet_num + 1):
        print(f"Computer's turn to attack (bullet {bullet}): ")

        while True:
            computers_bullet_row = random.randint(0, 9)
            computers_bullet_column = random.randint(0, 9)

            target = users_grid[computers_bullet_row][computers_bullet_column]

            if target == "X":  # Computer hit the user's ship
                print("\nHit! Computer hit part of your ship.")
                users_grid[computers_bullet_row][computers_bullet_column] = "H"  # Mark as hit
                print_board(users_grid)

                # check if the ship is sunk
                for ship in users_ships:
                    if (computers_bullet_row, computers_bullet_column) in ship["positions"]:
                        ship["hits"] += 1
                        if ship["hits"] == ship["length"]:
                            print(f"Computer sunk your {ship['name']}!")

                            # Mark the ship as sunk on the grid
                            for position in ship["positions"]:
                                users_grid[position[0]][position[1]] = "#"  # Mark as sunk
                            print_board(users_grid)
                            users_ships.remove(ship)  # Remove the ship from the list
                            
                            # Check if all user ships are sunk
                            if all(ship["hits"] == ship["length"] for ship in users_ships):
                                print("Game Over. Computer sunk all your ships!")
                                return users_grid, True  # Game over situation for all the ships sunk and all the bullets are fired
                            elif bullet_used == bullet_num:
                                print("pc has fired all of their bullets. Game over!")
                                return users_grid, False
                            break
            else:  # Computer missed and hit the water
                print("Miss! Computer hit the water.")
                users_grid[computers_bullet_row][computers_bullet_column] = "O"  # Mark as a miss on water
                print_board(users_grid)   # print updated grid after each shot
                break # to exite the loop after the miss
            # break removed for the loop to continue
        bullet_used += 1            
    # if all the bullets are finished game is over
    print("Computer's turn is over.")
    return users_grid, False
def main():

    # User places the ships
    users_grid = battleship_map()
    print("\nInitial Board:")
    print_board(users_grid, reveal= False)
    users_grid, users_ships = users_ships_positions(users_grid)

    # defining the pc's board
    pc_grid = battleship_map()

    # Computer places the ships
    """print("\ncomputers board:")"""
    pc_grid, pc_ships = computers_ships_positions(pc_grid, debug_mode = True)

    # Displaying the board with all ships placed (with computer's ships revealed)
    print("\nAll the ships have been placed. Here is the board for the game to start:")
    """print_board(pc_grid, reveal= False)"""

    # game loop
    user_turn = True
    while True:
        # Debugging statement to track the current turn
        print(f"\nCurrent turn: {'User' if user_turn else 'Computer'}")
        # users trun
        if user_turn:
            print("\nIt's your turn to attack the computers ships.")
            print_board(pc_grid, reveal = True)    # reveal true to show all the cells including pc's ships
            pc_grid, game_over = users_attack(pc_grid, pc_ships)
            if game_over:
                print("Game over!")
                break
        else:
        # computers turn 
            print("\nIts computers turn to attack your ships!")
            print_board(users_grid)
            users_grid, game_over = computers_attack(users_grid, users_ships)
            if game_over:
               print("Game over!")
               break
        user_turn = not user_turn    # to switch turns

    
if __name__ == "__main__":
    main()