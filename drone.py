from djitellopy import Tello
import time

# Constants
MAX_HEIGHT_CM = 150  # Maximum height in cm (1.5 meters)
STEP_CM = 20  # Distance to move in cm per command

def main():
    # Initialize the Tello drone
    tello = Tello()

    try:
        # Connect to the drone
        tello.connect()
        print(f"Connected to Tello. Battery Level: {tello.get_battery()}%")
        
        # Command-line control loop
        while True:
            print("\nCommands:")
            print("1: Takeoff")
            print("2: Land")
            print("3: Move Up")
            print("4: Move Down")
            print("5: Move Left")
            print("6: Move Right")
            print("7: Move Forwards")
            print("8: Move Backwards")
            print("q: Quit")
            
            # Get user input
            command = input("Enter your command: ").strip().lower()
            
            if command == "1":
                # Takeoff command
                try:
                    print("Taking off...")
                    tello.takeoff()
                    print("Drone is airborne.")
                    
                    # Check and limit height
                    current_height = tello.get_height()
                    print(f"Current Height: {current_height} cm")
                    
                    if current_height > MAX_HEIGHT_CM:
                        print(f"Height limit exceeded ({current_height} cm). Adjusting...")
                        tello.move_down(current_height - MAX_HEIGHT_CM)
                        print(f"Height adjusted to {MAX_HEIGHT_CM} cm.")
                except Exception as e:
                    print(f"Failed to take off: {e}")
            
            elif command == "2":
                # Land command
                try:
                    print("Landing...")
                    tello.land()
                    print("Drone has landed.")
                except Exception as e:
                    print(f"Failed to land: {e}")
            
            elif command == "3":
                # Move Up
                try:
                    print(f"Moving up by {STEP_CM} cm...")
                    tello.move_up(STEP_CM)
                except Exception as e:
                    print(f"Failed to move up: {e}")
            
            elif command == "4":
                # Move Down
                try:
                    print(f"Moving down by {STEP_CM} cm...")
                    tello.move_down(STEP_CM)
                except Exception as e:
                    print(f"Failed to move down: {e}")
            
            elif command == "5":
                # Move Left
                try:
                    print(f"Moving left by {STEP_CM} cm...")
                    tello.move_left(STEP_CM)
                except Exception as e:
                    print(f"Failed to move left: {e}")
            
            elif command == "6":
                # Move Right
                try:
                    print(f"Moving right by {STEP_CM} cm...")
                    tello.move_right(STEP_CM)
                except Exception as e:
                    print(f"Failed to move right: {e}")
            
            elif command == "7":
                # Move Forwards
                try:
                    print(f"Moving forwards by {STEP_CM} cm...")
                    tello.move_forward(STEP_CM)
                except Exception as e:
                    print(f"Failed to move forwards: {e}")
            
            elif command == "8":
                # Move Backwards
                try:
                    print(f"Moving backwards by {STEP_CM} cm...")
                    tello.move_back(STEP_CM)
                except Exception as e:
                    print(f"Failed to move backwards: {e}")
            
            elif command == "q":
                # Quit the program
                print("Exiting program...")
                break
            
            else:
                print("Invalid command. Please enter a valid option.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Ensure safe shutdown
        print("Ensuring the drone is landed...")
        try:
            tello.land()
        except Exception as e:
            print(f"Error during landing: {e}")
        
        print("Closing connection to the drone...")
        tello.end()

if __name__ == "__main__":
    main()
