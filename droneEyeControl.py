import os
import numpy as np
import pandas as pd
import pyautogui
import time
from sklearn.svm import SVC
from djitellopy import Tello
from screeninfo import get_monitors
import joblib
import keyboard  

MAX_HEIGHT_CM = 150
STEP_CM = 30
BUFFER_SIZE = 400

#convert system to 1080 x 1920 dimensions for uniformity
sys_height = get_monitors()[0].height
sys_width = get_monitors()[0].width
height_scale = 1080 / sys_height
width_scale = 1920 / sys_width

def initialize_drone():
    tello = Tello()
    tello.connect()
    print(f"Connected to Tello. Battery Level: {tello.get_battery()}%")
    return tello

# def normalize_data(df):
#     data = df[['x', 'y', 'x_avg', 'y_avg']].values.astype(np.float32)
#     return (data - data.min(axis=0) + 1) / (data.max(axis=0) - data.min(axis=0) + 1)

def collect_and_predict(data, classifier):
    df = pd.DataFrame(data)
    df["x_avg"] = df["x"].rolling(window=20, min_periods=1).mean()
    df["y_avg"] = df["y"].rolling(window=20, min_periods=1).mean()

    data = df[['x', 'y', 'x_avg', 'y_avg']].values.astype(np.float32)
    
    # normalized_data = normalize_data(df)
    # dont' normalize
    classification = classifier.predict([data.flatten()])[0]
    print(f"Predicted Gesture: {classification}")
    return classification

def execute_movement(tello, classification):
    try:
        current_height = tello.get_height()
        if current_height == 0:
            print("Drone is not airborne. Take off to enable movements.")
            return

        if classification == "up":
            print(f"Moving up by {STEP_CM} cm...")
            tello.move_up(STEP_CM)
        elif classification == "down":
            print(f"Moving down by {STEP_CM} cm...")
            tello.move_down(STEP_CM)
        elif classification == "left":
            print(f"Moving left by {STEP_CM} cm...")
            tello.move_left(STEP_CM)
        elif classification == "right":
            print(f"Moving right by {STEP_CM} cm...")
            tello.move_right(STEP_CM)
        elif classification == "upTwice":
            print(f"Moving forward by {STEP_CM} cm...")
            tello.move_forward(STEP_CM)
        elif classification == "downTwice":
            print(f"Moving backward by {STEP_CM} cm...")
            tello.move_back(STEP_CM)
        else:
            print("No valid gesture detected.")
    except Exception as e:
        print(f"Movement error: {e}")

def main():
    tello = initialize_drone()
    svm_classifier = joblib.load('models/svm_model.pkl')
    knn_classifier = joblib.load('models/knn_model.pkl')
    print("Machine Learning Model Loaded.")

    airborne = False
    data = {"x": [], "y": []}
    t = 0
    print("Commands: UP: Move eyes from center of screen to top and back to center")
    print("Commands: DOWN: Move eyes from center of screen to bottom and back to center")
    print("Commands: LEFT: Move eyes from center of screen to left and back to center")
    print("Commands: RIGHT: Move eyes from center of screen to right and back to center")
    print("Commands: FORWARD: Move eyes from center of screen to top and back to center TWICE")
    print("Commands: BACKWARDS: Move eyes from center of screen to bottom and back to center TWICE")

    print("Press t to takeoff, f to land:")

    pause = False

    try:
        while True:
            if not pause and keyboard.is_pressed('p'):  # 'P' for pause
                pause = True
                input(f"\n\n\nPausing, press ENTER to resume.\n\n\n")
                pause = False
                print("Resuming...\n\n")
                data = {"x": [], "y": []}
                t = 0
                time.sleep(1)
                print("Collecting gesture...")
                continue


            if keyboard.is_pressed('t'):  # 'T' for takeoff
                    try:
                        tello.takeoff()
                        print("Drone is airborne.")
                        print("Press t to takeoff, l to land. Collecting gesture...")
                        airborne = True
                    except Exception as e:
                        print(f"Takeoff failed: {e}")
             

            if keyboard.is_pressed('l'):  # 'L' for landing
                if airborne:
                    try:
                        tello.land()
                        print("Drone has landed.")
                        airborne = False
                    except Exception as e:
                        print(f"Landing failed: {e}")
                else:
                    print("Drone is already on the ground.")

            # Gesture recognition
            if airborne:
                
                x, y = pyautogui.position()
                data["x"].append(width_scale * x)
                data["y"].append(height_scale * y)
                t += 1
                time.sleep(0.01)  
                if t == BUFFER_SIZE:
                    classification = collect_and_predict(data, knn_classifier) # Swap to KNN if preferred
                    execute_movement(tello, classification)
                    data = {"x": [], "y": []}
                    t = 0

                    print("----")
            
    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the drone is landed and safely disconnected
        try:
            if airborne:
                tello.land()
        except Exception:
            pass
        tello.end()
        print("Connection to the drone closed.")

if __name__ == "__main__":
    main()
