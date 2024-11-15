import pyautogui
import time
import sys, os
from screeninfo import get_monitors
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import numpy as np
import pandas as pd


os.system('cls' if os.name == 'nt' else 'clear')
#convert system to 1080 x 1920 dimensions for uniformity
sys_height = get_monitors()[0].height
sys_width = get_monitors()[0].width
height_scale = 1080/sys_height
width_scale = 1920/sys_width

#store gesture data, 6 gesture types
up_data     = { "x":[], "y":[], "t":[] }
down_data   = { "x":[], "y":[], "t":[] }
left_data   = { "x":[], "y":[], "t":[] }
right_data  = { "x":[], "y":[], "t":[] }

gestures = ["up", "down", "left", "right", "noise"]

for gesture in gestures:
    #Record Gesture Countdown
    for i in range(10, 0, -1):
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tPlease look at the center of the screen")
        print("\t\t\t\t\t\t\tGesture Initializing in: ", i)
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')

    #Record Up Gesture
    for k in range(0,2): #CHANGE THIS TO PROPER RANGE FOR SAMPLE COLLECTION
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tPlease execute " + gesture + " gesture")
        time.sleep(0.5)
        os.system('cls' if os.name == 'nt' else 'clear')
        collection_time = 5
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tCollecting: ", collection_time)
        i = 0
        while True:

            x, y = pyautogui.position()
            up_data["x"].append(width_scale * x)
            up_data["y"].append(height_scale * y)
            up_data["t"].append(i/100)

            i += 1
            if i % 100 == 0:
                os.system('cls' if os.name == 'nt' else 'clear')
                collection_time -= 1
                print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tCollecting: ", collection_time)

            if i >= 525: break
            #100hz sampling rate
            time.sleep(0.01)

        #Save Gesture Data
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tCollection Complete, Saving Data")
        df = pd.DataFrame(up_data)
        df.to_csv(os.path.join(os.getcwd(), gesture + "_" + str(k) + '.csv'), index=False)
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
