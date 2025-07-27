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
    active_map = generate_random_map(15, 25) # Initialize with a random map
    
    while True:
        print("\n" + "+"+"-"*43+"+")
        print("| GridPath AI Control Menu                  |")
        print("+"+"-"*43+"+")
        print("| Pathfinding Agents (Goal: 'E')            |")
        print("|  1: Manual Control                        |")
        print("|  2: Greedy AI                             |")
        print("|  3: A* AI (Optimal Path)                  |")
        print("|-------------------------------------------")
        print("| Area Coverage Agents (Goal: Cover Area)   |")
        print("|  4: Wall Follower AI                      |")
        print("|  5: Frontier Exploration AI               |")
        print("|-------------------------------------------")
        print("| Reinforcement Learning Agents             |")
        print("|  6: Train Q-Learning Agent (Slow)         |")
        print("|  7: Run Trained Q-Learning Agent          |")
        print("|-------------------------------------------")
        print("| Simulation Options:                       |")
        print("|  (a)djust animation speed                 |")
        print("|-------------------------------------------")
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
            import tkinter as tk
            from tkinter import filedialog
            import os

            root = tk.Tk()
            root.withdraw() # Hide the main window

            # Set initial directory to the 'maps' folder
            initial_dir = os.path.join(os.getcwd(), 'maps')
            if not os.path.exists(initial_dir):
                os.makedirs(initial_dir) # Create if it doesn't exist

            filepath = filedialog.askopenfilename(
                initialdir=initial_dir,
                title="Select a map file",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.* ")]
            )
            
            if filepath:
                loaded_map = load_map_from_file(filepath)
                if loaded_map:
                    active_map = loaded_map
                else:
                    print("Returning to menu.")
            else:
                print("Map loading cancelled.")
            continue

        if choice == 'a':
            try:
                new_speed = float(input("Enter new animation speed (e.g., 0.05 for fast, 0.5 for slow): "))
                if new_speed < 0:
                    raise ValueError
                # Update the animation_speed for the next game instance
                # This will be picked up when a new Game object is created
                # or if we pass it to the existing game object if it's already running.
                # For simplicity, we'll apply it to the next game instance.
                # If a game is already running, its speed can be adjusted with 'f'/'s' keys.
                Game.animation_speed_override = new_speed # Store as a class attribute for now
                print(f"Animation speed set to {new_speed}.")
            except ValueError:
                print("Invalid speed. Please enter a positive number.")
            continue

        if choice not in ['1', '2', '3', '4', '5', '6', '7']:
            print("Invalid choice, please try again.")
            continue

        # Use the currently active_map for the game instance
        if active_map is None: # Fallback if no map is loaded/generated yet
            active_map = generate_random_map(15, 25)

        game = Game(active_map, color_map, non_walkable_tiles)
        if hasattr(Game, 'animation_speed_override'):
            game.animation_speed = Game.animation_speed_override # Apply override

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