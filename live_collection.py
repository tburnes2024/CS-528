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

import pyautogui
from screeninfo import get_monitors

import joblib

global svm_classifier

train = True # Train a model
active = False # Run live gesture recognition

os.system('cls' if os.name == 'nt' else 'clear')
#convert system to 1080 x 1920 dimensions for uniformity
sys_height = get_monitors()[0].height
sys_width = get_monitors()[0].width
height_scale = 1080/sys_height
width_scale = 1920/sys_width

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
        data = df[['x', 'y', 'x_avg', 'y_avg']].values.astype(np.float32)

        # Normalize data
        # data = (data - data.min(axis=0) + 1) / (data.max(axis=0) - data.min(axis=0) + 1)

        # Populate lists with normalized data and labels
        features.append(data.flatten())
        labels.append(filename.split("\\")[-1].split("_")[0])

    return np.array(features), np.array(labels)

def train_and_evaluate_svm(X_train, y_train, X_test, y_test, evaluation=True):
    # Create the SVM classifier
    global svm_classifier
    svm_classifier = SVC(kernel='rbf', probability=True)
    knn_classifier = KNeighborsClassifier(n_neighbors=3)

    # Train the classifier
    svm_classifier.fit(X_train, y_train)
    knn_classifier.fit(X_train, y_train)

    if evaluation:
        # Evaluate the classifier
        y_pred = svm_classifier.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f'SVM accuracy: {accuracy:.3%}')

        conf_matrix = confusion_matrix(y_test, y_pred)
        sns.heatmap(conf_matrix, annot=True, cmap="Blues", xticklabels=svm_classifier.classes_, yticklabels=svm_classifier.classes_)
        plt.title('train')
        plt.xlabel('pred')
        plt.ylabel('actual')
        plt.show()

        y_pred = knn_classifier.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f'SVM accuracy: {accuracy:.3%}')

        conf_matrix = confusion_matrix(y_test, y_pred)
        sns.heatmap(conf_matrix, annot=True, cmap="Blues", xticklabels=svm_classifier.classes_, yticklabels=svm_classifier.classes_)
        plt.title('train')
        plt.xlabel('pred')
        plt.ylabel('actual')
        plt.show()
    
    # Save model to a file for later use
    joblib.dump(svm_classifier, 'models/svm_model.pkl')
    joblib.dump(svm_classifier, 'models/knn_model.pkl')

#initialize and train SVM
if train:
    # Load the dataset
    train_labels = pd.read_csv("./train.csv")
    test_labels = pd.read_csv("./validate.csv")
    all_labels = pd.read_csv("./all_train.csv")
    train_dir = "./dataset" 

    # Create the train and test sets
    X_train, y_train = load_data(train_labels, train_dir)
    X_test, y_test = load_data(test_labels, train_dir)
    x_all, y_all = load_data(all_labels, train_dir)

    # Perform training with SVM. Change boolean for evaluation and passed-in data if necessary.
    train_and_evaluate_svm(x_all, y_all, X_test, y_test, evaluation=False)

if active:
    # Load model
    svm_classifier = joblib.load('svm/svm_model.pkl')

    #Enter Data Collection Loop
    input("Press enter to proceed with live gesture recognition")

    # acc_data  = { "x":[], "y":[], "z":[]}
    # gyro_data = { "x":[], "y":[], "z":[]}
    t = 0
    # acc_t = 0
    # mpu_6050 = serial.Serial('COM8', 115200)
    data = {"x":[], "y":[]}

    while(1):

        x, y = pyautogui.position()
        data["x"].append(width_scale * x)
        data["y"].append(height_scale * y)
        t += 1
        time.sleep(0.01)

        #If 4 seconds of data is collected run prediction, reset buffer and 
        # immediately begin new gesture recognition    
        if t == 400:
            df = pd.DataFrame(data)
            x_avg = []
            y_avg = []
            for idx, x in enumerate(data["x"]):
                if idx < 19:
                    x_avg.append(df["x"][idx: idx+20].sum()/20)
                else:
                    x_avg.append(df["x"][idx-19: idx+1].sum()/20)
            for idx, y in enumerate(df["y"]):
                if idx < 19:
                    y_avg.append(df["y"][idx: idx+20].sum()/20)
                else:
                    y_avg.append(df["y"][idx-19: idx+1].sum()/20)
            df["x_avg"] = x_avg
            df["y_avg"] = y_avg
            # Normalize data
            data = df[['x', 'y', 'x_avg', 'y_avg']].values.astype(np.float32)
            # data = (data - data.min(axis=0) + 1) / (data.max(axis=0) - data.min(axis=0) + 1)
            os.system('cls' if os.name == 'nt' else 'clear')

            df["x_avg"] = x_avg
            df["y_avg"] = y_avg
            time.sleep(0.2)
            print(svm_classifier.predict([data.flatten()])[0])
            probs = svm_classifier.predict_proba([data.flatten()])
            # print(probs)
            # print(svm_classifier.classes_)
            # gestures = ["down", "left", "right", "up"]
            # if probs[0][3] > 0.66:
            #     print('undetected')
            # else:
            #     print(gestures[np.argmax(np.append(probs[0 , 0:3], probs[0, -1]))])
            print(probs)

            data  = { "x":[], "y":[]}
            t = 0
            time.sleep(1)
            print("----")
            