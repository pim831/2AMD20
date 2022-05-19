import pandas as pd
import numpy as np
from pathlib import Path 

in_path = "Data_Cleaning/Raw_datasets/News_Papers/"
out_path = "Data_Cleaning/Cleaned_datasets/News_Papers/"

# Read Data
News_Reports = pd.read_excel(in_path + "Resultaten sentimentanalyse zonder koppen.xlsx", index_col=0)
# Drop (seemingly) useless Rows
News_Reports.drop(['Unnamed: 2', 'Bevat corona', 'True = 1', "Gemiddelde gisteren"], axis=1, inplace=True)


# Daily summations
Daily_summations = News_Reports.groupby("Datum").sum().reset_index()