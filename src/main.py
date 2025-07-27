from src.utils.map_utils import generate_random_map, load_map_from_file
from src.game.game import Game
from src.agents.greedy_agent import GreedyAgent
from src.agents.a_star_agent import AStarAgent
from src.agents.wall_follower_agent import WallFollowerAgent
from src.agents.frontier_agent import FrontierAgent
from src.agents.q_learning_runner import QLearningRunner

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
    
    while True:
        print("\n" + "+"+"-"*43+"+")
        print("| GridPath AI Control Menu                  |")
        print("+"+"-"*43+"+")
        print("| Pathfinding Agents (Goal: 'E')            |")
        print("|  1: Manual Control                        |")
        print("|  2: Greedy AI                             |")
        print("|  3: A* AI (Optimal Path)                  |")
        print("|-------------------------------------------|")
        print("| Area Coverage Agents (Goal: Cover Area)   |")
        print("|  4: Wall Follower AI                      |")
        print("|  5: Frontier Exploration AI               |")
        print("|-------------------------------------------|")
        print("| Reinforcement Learning Agents             |")
        print("|  6: Train Q-Learning Agent (Slow)         |")
        print("|  7: Run Trained Q-Learning Agent          |")
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

        if choice not in ['1', '2', '3', '4', '5', '6', '7']:
            print("Invalid choice, please try again.")
            continue

        # Generate a new map for each simulation to ensure a clean state
        active_map = generate_random_map(15, 25) # You can adjust map size here
        game = Game(active_map, color_map, non_walkable_tiles)

        if choice == '1':
            # Manual control is handled directly in Game, not by an agent class
            game.run_manual()
        elif choice == '2':
            agent = GreedyAgent(game)
            agent.run()
        elif choice == '3':
            agent = AStarAgent(game)
            agent.run()
        elif choice == '4':
            agent = WallFollowerAgent(game)
            agent.run()
        elif choice == '5':
            agent = FrontierAgent(game)
            agent.run()
        elif choice == '6':
            runner = QLearningRunner(game)
            runner.run(training_mode=True)
        elif choice == '7':
            runner = QLearningRunner(game)
            runner.run(training_mode=False)
        
        # If the game requested a new map, it will be handled by the next loop iteration
        # Otherwise, the loop continues to show the menu again.


if __name__ == "__main__":
    main()
