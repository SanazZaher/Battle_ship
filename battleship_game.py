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
user_bullet_used = 0   
pc_bullet_used = 0

def battleship_map():
    """Generates a 10x10 grid for the battleship game."""
    grid = []
    for i in range(10):   # looping through each row
        row = []
        for j in range(10):    # looping through each column
            row.append(".")
        grid.append(row)
    return grid

def print_board(grid, reveal= True):
    """Prints the board with row numbers, column letters, and ships marked with 'X'."""
    print(" ", end=" ")    # Printing the column letters
    for letter in column_letters.keys():  
        print(letter, end=" ")
    print()

    for i in range(len(grid)):    # Printing each row with numbers
        print(i, end=" ")  
        for j in range(len(grid[i])):
            if not reveal and grid[i][j] == "P":  # If not reveal mode and grid cell has a PC ship, print "." instead, meaning hide the computes ships.
                print(".", end=" ")
            else:
                print(grid[i][j], end=" ")
        print()

def check_overlap(grid, positions):
    """Check for overlap with existing ships."""
    for row, col in positions:
        if grid[row][col] != ".":
            return True
    return False

def check_adjacency(grid, positions):
    """Check for adjacency with existing ships."""
    for row, col in positions:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < 10 and 0 <= nc < 10 and grid[nr][nc] != ".":
                    return True
    return False

def users_ships_positions(users_grid):
    """Allows the user to place their ships on the grid."""
    ships = []   # list to store the ships
    ship_info = [ ("Battleship", 4), ("Cruiser", 3), ("Destroyer", 2)]  # List of tuples with Cell lengths of the 5 ships and their names
    
    for ship_name, length in ship_info: # tuple unpacking
        print(f"Where do you want {ship_name} (length:{length})?")
        while True:
            try:
                # Row
                while True:
                    row = int(input("Choose a number from 0-9 for the row position of your ship:"))
                    if 0 <= row <= 9:     # checking if the user entered a valid number for row 
                        break
                    else:
                        print("Invalid row. Please choose a number from 0 to 9 for the row.")

                while True:
                    # column
                    user_column = input("Choose a letter from A-J for the column position of your ship:").upper()
                    if user_column in column_letters:     # getting the key value of each letter from dictionary and checking if it's valid 
                        column = column_letters[user_column]
                        break
                    else:
                        print("Invalid column. Please choose a capital letter from A to J.")

                while True:
                    # orientation
                    users_ships_orientation = input("Choose orientation (H for horizontal, V for vertical): ").upper()
                    if users_ships_orientation == "H":
                        if column + length > 10:
                            raise ValueError("Invalid ship placement. Ship goes out of grid.")
                        positions = [(row, column + i) for i in range(length)]   # making a list of positions
                    elif users_ships_orientation == "V":
                        if row + length > 10:
                            raise ValueError("Invalid ship placement. Ship goes out of grid.")
                        positions = [(row + i, column) for i in range(length)]
                    else:
                        print("Invalid orientation. Please choose H for horizontal or V for vertical.")
                        continue

                    if check_overlap(users_grid, positions):
                        raise ValueError("Invalid ship placement. Overlaps with existing ship.")
                    if check_adjacency(users_grid, positions):
                        raise ValueError("Invalid ship placement. Adjacent to existing ship.")
                    
                    # No overlap or adjacency, add the ship to the list and mark its positions on the grid
                    ships.append({"name": ship_name, "length": length, "positions": positions, "hits": 0})
                    for position in positions:
                        users_grid[position[0]][position[1]] = "X"
                    print("\nCurrent Board:")
                    print_board(users_grid)
                    break  # Exit the loop if ship placement is successful

                break  # Exit the loop if ship placement is successful

            except ValueError as e:
                print(e)
                print("Please choose a different position.")
    return users_grid, ships

def computers_ships_positions(pc_grid, users_grid, debug_mode = False):  
    """Places the computer's ships randomly on the separate grid and this won't be revealed to the user."""   
    # Adding the debug mode for the PC ships to not display them on the board
    pc_ships_placed = 0    # to track the number of ships placed
    pc_ships = []
    ship_info = [("Battleship", 4), ("Cruiser", 3), ("Destroyer", 2)]  # List of Cell lengths of the 3 ships and their names

    for ship_name, length in ship_info:   # iterating over each ship to place them on the grid
        ship_placed = False   # to check if the ship is placed successfully
        while not ship_placed:
            try:
                positions = []
                # Row
                while True:
                    row = random.randrange(0, 10)
                    if 0 <= row <= 9:
                        break
                # Column
                while True:
                    column = random.randrange(0, 10)
                    if 0 <= column <= 9:
                        break

                # Orientation
                pc_ships_orientation = random.choice(["H", "V"])    # random choice for orientation
                
                if pc_ships_orientation == "H":
                    if column + length <= 10:    # not to place it out of the grid 
                        positions = [(row, column + i) for i in range(length)]
                elif pc_ships_orientation == "V":
                    if row + length <= 10:
                        positions = [(row + i, column) for i in range(length)]
                else:
                    raise ValueError("Invalid orientation.")

                if check_overlap(pc_grid, positions) or check_overlap(users_grid, positions):
                    continue  # Overlap detected, prompt PC to choose a different position
                if check_adjacency(pc_grid, positions) or check_adjacency(users_grid, positions):
                    continue  # Adjacent to existing ship, prompt PC to choose a different position
                
                # No overlap or adjacency, add the ship to the list and mark its positions on the grid
                pc_ships.append({"name": ship_name, "length": length, "positions": positions, "hits": 0})
                for position in positions:
                    pc_grid[position[0]][position[1]] = "P"
                ship_placed = True   # Ship placed successfully
            except ValueError:
                continue  # Continue to prompt PC to choose a different position

        pc_ships_placed += 1

    return pc_grid, pc_ships

# Define the function to determine the current turn
def get_current_turn(turn_count):
    return turn_count % 2 == 0  # Even turns correspond to the user's turn, odd turns correspond to the computer's turn

# step 4
def users_attack(pc_grid, pc_ships, turn_count):
    """Allows the user to guess the computer's ship positions and remove them from the grid."""
    bullet_num = 20
    global user_bullet_used
    while turn_count % 2 == 0:    #as long as turn count is an even number its users turn 
        print(f"\nLet's attack! Where do you want to shoot your bullet {user_bullet_used + 1} at? ")

        # Get user input for row
        while True:   # to control the number of bullets fired by the user
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
                        if not pc_ships:
                            print("Congratulations! You've sunk all the computer's ships!")
                            return pc_grid, True   # game over situation is if all the ships are sunk or if all the bullets are fired
                        break   
        else:  # User missed and hit the water
            print("\nMiss! You hit the water.")
            pc_grid[users_bullet_row][users_bullet_column] = "O"  # Mark as a miss on water 
            print_board(pc_grid)  # Print the updated grid after each shot 
        user_bullet_used += 1   #increment the bullet used      
        turn_count +=1   # increment the turn count after this bullet
    if bullet_num == user_bullet_used:
        # If all bullets are fired and all ships are not sunk, the game is over
        print("You've used all your bullets. Game over.")
    return pc_grid, False

# step 5
def computers_attack(users_grid, users_ships,turn_count):
    """Computer attacks the user's grid randomly and gives the updated board."""
    bullet_num = 20
    global pc_bullet_used
    while turn_count % 2 != 0 :    # as long as turn count is an odd number it's pc's turn
        print(f"Computer's turn to attack bullet {pc_bullet_used +1 }: ")

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
                        elif pc_bullet_used == bullet_num:
                            print("pc has fired all of their bullets. Game over!")
                            return users_grid, False
                        break
        else:  # Computer missed and hit the water
            print("Miss! Computer hit the water.")
            users_grid[computers_bullet_row][computers_bullet_column] = "O"  # Mark as a miss on water
            print_board(users_grid)   # print updated grid after each shot
            break # to exite the loop after the miss
        # break removed for the loop to continue
    pc_bullet_used += 1 
    turn_count +=1     
    if bullet_num == pc_bullet_used:       
        # if all the bullets are finished game is over
        print("Computer's turn is over.")
    return users_grid, False


def main():
    turn_count = 0  # Initialize turn count

    # User places the ships
    users_grid = battleship_map()
    print("\nInitial Board:")
    print_board(users_grid, reveal = False)
    users_grid, users_ships = users_ships_positions(users_grid)   # allow the user to print thei ships on the grid

    # defining the pc's board
    pc_grid = battleship_map()

    # Computer places the ships
    pc_grid, pc_ships = computers_ships_positions(pc_grid, users_grid, debug_mode= False)   # passing the reveal argument as false to hide pc's ships

    # Displaying the board with all ships placed (with computer's ships revealed)
    print("\nAll the ships have been placed. Here is the board for the game to start:")

    # game loop
    game_over = False
    while True:   # start the loop until the game is over

        # Debugging statement to track the current turn
        print(f"\nCurrent turn: {'User' if get_current_turn(turn_count) else 'Computer'}")

        # User's turn
        if turn_count % 2 == 0:
            print("\nIt's your turn to attack the computer's ships.")
            print_board(pc_grid, reveal= False)  # reveal true to show all the cells including pc's ships
            pc_grid, game_over = users_attack(pc_grid, pc_ships, turn_count)
            turn_count += 1
            if game_over:
                print("You lost, game over!")
                break

        # Computer's turn (when turn_count is odd)
        elif turn_count % 2 != 0:
            print("\nIt's the computer's turn to attack your ships!")
            print_board(users_grid)
            users_grid, game_over = computers_attack(users_grid, users_ships, turn_count)
            turn_count += 1
            if game_over:
                print("Computer lost!")
                break
        else:
            break

    print("Game Ended!")

if __name__ == "__main__":
    main()
