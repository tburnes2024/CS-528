import pandas as pd
import random

trainProp = 0.8
numData = 61

# Generate all filenames for each category
categories = ['down', 'up', 'noise', 'left', 'right']
files = []

# Create filenames for each category from 0 to 60
for i in range(len(categories)):
    files.append([])
    for j in range(numData):  # From 0 to 60 inclusive
        files[i].append(f'{categories[i]}_{j}')
    random.shuffle(files[i])

# # Shuffle the filenames
# random.shuffle(files)

# Calculate the split index
train_size = int(trainProp * numData)
train_files = []
validate_files = []

for category in files:
    train_files.extend(category[:train_size])
    validate_files.extend(category[train_size:])

train_files = {"filename" : train_files}
validate_files = {"filename" : validate_files}
train_df = pd.DataFrame(train_files)
validate_df = pd.DataFrame(validate_files)

# Save the DataFrames to CSV
train_df.to_csv('train.csv', index=False)
validate_df.to_csv('validate.csv', index=False)

print("train.csv and validate.csv have been created.")
