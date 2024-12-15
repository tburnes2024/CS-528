file = open("all_train.csv", "w")
gestures = ["left", "right", "up", "down", "noise", "upTwice", "downTwice"]
file.write("filename\n")
# Write file names to all_train.csv
for gesture in gestures:
    for i in range(0, 81):
        file.write(gesture + "_" + str(i) + "\n")
# Write extra 10 left gestures to all_train.csv
for i in range(61, 71):
    file.write("left_" + str(i) + "\n")