import os
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.svm import SVC
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import serial 
import time 
import sys

global svm_classifier


# Function to load dataset
def load_data(label_df, data_dir):
    # Empty lists to store features and labels
    features = []
    labels = []

    for _, row in label_df.iterrows():
        filename = os.path.join(data_dir, row['filename'] + ".csv")

        # Read file into pandas dataframe
        df = pd.read_csv(filename)

        # Keep only accelerometer and gyroscope signals
        data = df[['acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z']].values.astype(np.float32)

        # Normalize data
        data = (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0))

        # Populate lists with normalized data and labels
        features.append(data.flatten())
        labels.append(filename.split("\\")[-1].split("_")[0])

    return np.array(features), np.array(labels)

def train_and_evaluate_svm(X_train, y_train):
    # Create the SVM classifier
    global svm_classifier
    svm_classifier = SVC(kernel='rbf', probability=True)

    # Train the classifier
    svm_classifier.fit(X_train, y_train)

#initialize and train SVM
train_labels = pd.read_csv("C:\\Users\\tburnes\\Documents\\ESP\\all_train.csv") 
train_dir = "C:\\Users\\tburnes\\Documents\\ESP\\data" 

# Create the train and test sets
X_train, y_train = load_data(train_labels, train_dir)

# Perform training with SVM
train_and_evaluate_svm(X_train, y_train)

#Enter Data Collection Loop
input("Press enter to proceed with live gesture recognition")


acc_data  = { "x":[], "y":[], "z":[]}
gyro_data = { "x":[], "y":[], "z":[]}
gyro_t = 0
acc_t = 0
mpu_6050 = serial.Serial('COM8', 115200)
while(1):

    data = mpu_6050.readline().decode('utf-8')  
    parsed_data = data.split()

    if len(parsed_data) > 2 and parsed_data[2] == "DATA_ACC:":
        
        #print("Acceleration data:", parsed_data[3], parsed_data[4], parsed_data[5])
        acc_data["x"].append(parsed_data[3])
        acc_data["y"].append(parsed_data[4])
        acc_data["z"].append(parsed_data[5])
        acc_t += 1
    if len(parsed_data) > 2 and parsed_data[2] == "DATA_GYRO:":
        #print("Gyroscopic data:", parsed_data[3], parsed_data[4], parsed_data[5])
        gyro_data["x"].append(parsed_data[3])
        gyro_data["y"].append(parsed_data[4])
        gyro_data["z"].append(parsed_data[5])
        gyro_t += 1

    #If 4 seconds of data is collected run prediction, reset buffer and 
    # immediately begin new gesture recognition    
    if gyro_t == acc_t and acc_t == 400:
        data = {}
        data["acc_x"] = acc_data["x"]
        data["acc_y"] = acc_data["y"]
        data["acc_z"] = acc_data["z"]
        data["gyro_x"] = gyro_data["x"]
        data["gyro_y"] = gyro_data["y"]
        data["gyro_z"] = gyro_data["z"]
        df = pd.DataFrame(data)
        data = df[['acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z']].values.astype(np.float32)
        # Normalize data
        data = (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0))
        os.system('cls' if os.name == 'nt' else 'clear')
        time.sleep(0.2)
        #print(svm_classifier.predict([data.flatten()])[0])
        probs = svm_classifier.predict_proba([data.flatten()])
        # print(probs)
        # print(svm_classifier.classes_)
        gestures = ["down", "left", "right", "up"]
        if probs[0][3] > 0.66:
            print('undetected')
        else:
            print(gestures[np.argmax(np.append(probs[0 , 0:3], probs[0, -1]))])

        acc_data  = { "x":[], "y":[], "z":[]}
        gyro_data = { "x":[], "y":[], "z":[]}
        gyro_t = 0
        acc_t = 0
        time.sleep(0.5)
        print("----")
        mpu_6050.reset_input_buffer()
        