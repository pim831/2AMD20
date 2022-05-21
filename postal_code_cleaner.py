import pandas as pd
import numpy as np
import csv

raw_data = pd.read_csv("Enexis_net.csv", index_col=0)

# Filter out rows without data
raw_data = raw_data[raw_data["Color"] != "No Info"].reset_index()

raw_data.drop(["index"], axis=1, inplace=True)

raw_data.to_csv("Clean_Enexis_net.csv")