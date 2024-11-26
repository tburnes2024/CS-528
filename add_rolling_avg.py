import os
import numpy
import pandas


files = os.listdir('dataset')

for file in files:
    path = os.path.join('dataset', file)
    df = pandas.read_csv(path)
    x_avg = []
    y_avg = []
    for idx, x in enumerate(df["x"]):
        if idx < 4:
            x_avg.append(x)
        else:
            x_avg.append(df["x"][idx-4: idx+1].sum()/5)


    for idx, y in enumerate(df["y"]):
        if idx < 4:
            y_avg.append(y)
        else:
            y_avg.append(df["y"][idx-4: idx+1].sum()/5)

    df["x_avg"] = x_avg
    df["y_avg"] = y_avg
    df.to_csv(path, index=False)
