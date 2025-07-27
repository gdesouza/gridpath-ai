from map_utils import generate_random_map, load_map_from_file
from game import Game

def main():
    """
    Main function to run the GridPath AI application.

    This function initializes the game, handles user interaction through a menu,
    and orchestrates the execution of different game modes (manual, AI).
    """
    color_map = {
        '.': '#d3d3d3', 'V': '#fef08a', 'P': '#3498db',
        'E': '#2ecc71', 'X': '#34495e'
    }
    non_walkable_tiles = {'X'}
    active_map = generate_random_map(15, 25)

    while True:
        print("\n" + "+"+"-"*43+"+")
        print("| GridPath AI Control Menu                  |")
        print("+"+"-"*43+"+")
        print("| 1: Manual Control                 |")
        print("| 2: Greedy AI                      |")
        print("| 3: A* AI (Optimal)                |")
        print("|-------------------------------------------|")
        print("| Map Options:                              |")
        print("|  (l)oad map, (n)ew random map, (e)xit     |")
        print("+"+"-"*43+"+")
        choice = input("Enter your choice: ").lower()

        if choice == 'e':
            print("Exiting program.")
            break
        
        if choice == 'n':
            active_map = generate_random_map(15, 25)
            continue

        if choice == 'l':
            filepath = input("Enter the path to the map file: ")
            loaded_map = load_map_from_file(filepath)
            if loaded_map:
                active_map = loaded_map
            else:
                print("Returning to menu.")
            continue

        if choice not in ['1', '2', '3']:
            print("Invalid choice, please try again.")
            continue

        game = Game(active_map, color_map, non_walkable_tiles)

        if choice == '1':
            game.run_manual()
        elif choice == '2':
            game.run_greedy_ai()
        elif choice == '3':
            game.run_a_star_ai()
        
        if game.request == 'NEW_MAP':
            active_map = generate_random_map(15, 25)

if __name__ == "__main__":
    main()
