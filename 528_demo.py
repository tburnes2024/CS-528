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


#Record Gesture Countdown
for i in range(10, 0, -1):
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tPlease look at the center of the screen")
    print("\t\t\t\t\t\t\tGesture Initializing in: ", i)
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')

#Record Up Gesture
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tPlease execute up gesture")
time.sleep(0.5)
os.system('cls' if os.name == 'nt' else 'clear')
collection_time = 5
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\t\t\t\tCollecting: ", collection_time)
i = 0
while True:

    x, y = pyautogui.position()
    up_data["x"].append(x)
    up_data["y"].append(y)
    up_data["t"].append(i/100)

    i += 1
    if i % 100 == 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        collection_time -= 1
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\t\t\t\tCollecting: ", collection_time)

    if i >= 525: break
    #100hz sampling rate
    time.sleep(0.01)

#Display Gesture Graph
os.system('cls' if os.name == 'nt' else 'clear')
print("Collection Complete, Analyzing Data")
plt.plot(up_data["t"], up_data["x"],linestyle='-', color='b', label='x')
plt.plot(up_data["t"], up_data["y"], linestyle='-', color='g', label='y')

#Add titles and labels
plt.title("Eye Tracking Gesture Plot")
plt.xlabel('Time')
plt.ylabel('Position')

# Add a legend
plt.legend()
plt.show()

#Display Gesture FFT
N = 525
T = 1.0/100.0

x = np.linspace(0.0, N*T, N, endpoint = False)
xf = fftfreq(N, T)[:N//2]
plt.plot(xf, 2.0/N * np.abs(fft(np.array(up_data["x"]))[0:N//2]), color = 'g', label = 'y')
plt.plot(xf, 2.0/N * np.abs(fft(np.array(up_data["y"]))[0:N//2]), color = 'b', label = 'z')
plt.title('FFT of Eye Tracking Gesture')
plt.legend()
plt.grid()
plt.show()

#Save Gesture Data
