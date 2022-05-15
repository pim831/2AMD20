import pandas as pd
import numpy as np
from pathlib import Path 

in_path = "Raw_datasets/RIVM_datasets/"
out_path = "Cleaned_datasets/RIVM_datasets/"

# municipality_count = pd.read_csv(data_path + "COVID-19_aantallen_gemeente_cumulatief.csv", sep=";") # seems useless when also looking at daily count
municipality_daily_count = pd.read_csv(in_path + "COVID-19_aantallen_gemeente_per_dag.csv", sep=";")
ic_count = pd.read_csv(in_path + "COVID-19_ic_opnames.csv", sep=";")

# Drop Useless rows
municipality_daily_count.drop(["Version", "Date_of_report"], axis=1, inplace=True)


# Get national daily count of cases
national_daily_count = municipality_daily_count.groupby("Date_of_publication").sum().reset_index()



def RowIncrease(target, columnName, df):
    """Add column to a given dataframe which states if the target value has increased compared to the previous row

    Args:
        target (String): Column containing the values to look at
        columnName (String): Name of the new column
        df (DataFrame): DataFrame to adept

    Returns:
        Dataframe: resulting DataFrame with the added column named columnName
    """        
    df[columnName] = np.nan 
    for i in range(1, len(df)):
        df.loc[i, columnName] = df.loc[i-1, target] < df.loc[i, target]
    return df

# Add increase over day for Reported cases and deaths to nation_daily_count
national_daily_count = RowIncrease("Total_reported", "Cases_Increase", national_daily_count)
national_daily_count = RowIncrease("Deceased", "Deaths_Increase", national_daily_count)

# Add increase over day for IC admissions
ic_count = RowIncrease("IC_admission", "Admission_Increase", ic_count)



# Write cleaned datasets to csv
national_daily_count.to_csv(out_path + "Daily_Count.csv")
ic_count.to_csv(out_path + "IC_Count.csv")