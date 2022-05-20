import pandas as pd
import numpy as np
from pathlib import Path 

in_path = "Data_Cleaning/Raw_datasets/News_Papers/"
out_path = "Data_Cleaning/Cleaned_datasets/News_Papers/"

# Read Data
News_Reports = pd.read_excel(in_path + "Resultaten sentimentanalyse zonder koppen.xlsx", index_col=0)
# Drop (seemingly) useless Rows
News_Reports.drop(['Unnamed: 2', 'Bevat corona', 'True = 1', "Gemiddelde gisteren", "Datum.1", 
        "Dagen sinds 1 maart 20", "URL", "Pattern", "Positive count", "Negative count", 
        "Anger count", "Disgust count", "Fear count", "Joy count", "Sadness count", 
        "Pattern: Emotionaliteit", "Pattern rounded", "Week", "Year", "Month", 
        "Neg <-.5", "Pos >.5", "Words"], axis=1, inplace=True)


# Daily summations
Daily_summations = News_Reports.groupby("Datum").size().reset_index()
Daily_summations.rename(columns={0:'News Paper count'}, inplace=True)


# News_Reports Column Renaming

News_Reports.rename(columns={'Positive list':'Positive word'}, inplace=True)
News_Reports.rename(columns={'Negative list':'Negative word'}, inplace=True)
News_Reports.rename(columns={'Anger list':'Anger word'}, inplace=True)
News_Reports.rename(columns={'Disgust list':'Disgust word'}, inplace=True)
News_Reports.rename(columns={'Fear list':'Fear word'}, inplace=True)
News_Reports.rename(columns={'Joy list':'Joy word'}, inplace=True)
News_Reports.rename(columns={'Sadness list':'Sadness word'}, inplace=True)

News_Reports.to_csv(out_path + "News_Reports.csv")
Daily_summations.to_csv(out_path + "Daily_News_Count.csv")