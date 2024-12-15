import os
import numpy
import pandas


files = os.listdir('dataset')

for file in files:
    path = os.path.join('dataset', file)
    df = pandas.read_csv(path)
    x_avg = []
    y_avg = []
    # for idx, x in enumerate(df["x"]):
    #     if idx < 19:
    #         x_avg.append(df["x"][idx: idx+20].sum()/20)
    #     else:
    #         x_avg.append(df["x"][idx-19: idx+1].sum()/20)


    # for idx, y in enumerate(df["y"]):
    #     if idx < 19:
    #         y_avg.append(df["y"][idx: idx+20].sum()/20)
    #     else:
    #         y_avg.append(df["y"][idx-19: idx+1].sum()/20)
    df["x_avg"] = df["x"].rolling(window=20, min_periods=1).mean()
    df["y_avg"] = df["y"].rolling(window=20, min_periods=1).mean()

    # df["x_avg"] = x_avg
    # df["y_avg"] = y_avg
    df.to_csv(path, index=False)
