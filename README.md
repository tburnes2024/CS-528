# Title

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [API](#api)
- [Contributing](#contributing)


## Background


## Install

This code requires the following python libraries to operate

```
os
numpy
pandas
pyautogui
time
sklearn
djitellopy
screeninfo
joblib
keyboard  
```

### Any optional sections

## Usage
I will list how to use the most fundamental scripts to the project. Most of the scripts in the repo will not need to be accessed and were mostly used for testing and collecting training data for the model.

**live_collection.py**
  Use this to test live gesture recognition. Initiate and calibrate GazePointer to control the mouse position. Then run the script with the terminal full screen. When the bar appears below the last predicted gesture this is the indication for you to begin recording your next gesture. You can also run this just using your mouse as the script tracks the position of your cursor on the screen.

**droneEyeControl.py**
  Use this to combine live gesture recognition with drone movements. First Initiate and calibrate GazePointer to control the mouse position. Then connect your tello drone and run the script. Be careful to look where your cursor goes as you click around the screen connecting the tello drone because GazePointer recalibrates the gaze as you click and this setting cannot be turned off. You will likely notice some drift as you use the script, so this often cannot be used for extended periods of time.

**Dataset**
  Contains training data

**Models**
  Contains most recent SVM and KNN models that are loaded in for live testing.


### See our Live Demo on Youtube!
KNN Model(better model): https://www.youtube.com/watch?v=nPddyZN4p3M

SVM Model: https://www.youtube.com/watch?v=Tm17ogwmUQo


[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/YOUTUBE_VIDEO_ID_HERE/0.jpg)](https://www.youtube.com/watch?v=Tm17ogwmUQo)



