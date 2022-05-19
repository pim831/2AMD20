import pandas as pd
import numpy as np
from pathlib import Path 

in_path = "Data_Cleaning/Raw_datasets/RIVM_datasets/"
out_path = "Data_Cleaning/Cleaned_datasets/RIVM_datasets/"

# municipality_count = pd.read_csv(data_path + "COVID-19_aantallen_gemeente_cumulatief.csv", sep=";") # seems useless when also looking at daily count
municipality_daily_count = pd.read_csv(in_path + "COVID-19_aantallen_gemeente_per_dag.csv", sep=";")
ic_count = pd.read_csv(in_path + "COVID-19_ic_opnames.csv", sep=";")

# Drop Useless rows
municipality_daily_count.drop(["Version", "Date_of_report"], axis=1, inplace=True)
ic_count.drop(["Version", "Date_of_report", "IC_admission_notification"], axis=1, inplace=True)

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
    for i in range(13, len(df)):
        df.loc[i, columnName] = df.loc[i-13:i-7, target].mean() < df.loc[i-6:i, target].mean()
    return df

# Add increase over day for Reported cases and deaths to nation_daily_count
national_daily_count = RowIncrease("Total_reported", "Cases_Increase", national_daily_count)
national_daily_count = RowIncrease("Deceased", "Deaths_Increase", national_daily_count)

# Add increase over day for IC admissions
ic_count = RowIncrease("IC_admission", "Admission_Increase", ic_count)

# Add categories to group numerical data:
def add_category_data(df, column_name, category_name, placement, intervals):
    """Add a categorical column based on a numerical column to subdivided the numerical values into ranges

    Args:
        df (DataFrame): Dataframe to adept
        column_name (String): Name of the column containing numerical data
        category_name (String): Name of the new categorical column
        placement (Int): Placement of the new column in the dataframe
        intervals ([Int]): Intervals to mark where you shift to a next category
    """    
    bins = [df[column_name].min()-1]
    for i in intervals:
        bins.append(i)
    bins.append(1+df[column_name].max())
    category = pd.cut(df[column_name], bins=bins, labels=['Very Low', 'Low', 'Intermediate', 'High', 'Very High'])
    df.insert(placement, category_name, category)

# IC data
add_category_data(ic_count, "IC_admission","IC_admission_level", 2, [5,20,40,70])
# Cases/Deaths data
add_category_data(national_daily_count, "Total_reported", "Cases_level", 2, [250,2500,10000,20000])
add_category_data(national_daily_count, "Deceased", "Deaths_level", 4, [10,25,50,125,])



# Write cleaned datasets to csv
national_daily_count.to_csv(out_path + "Daily_Count.csv")
ic_count.to_csv(out_path + "IC_Count.csv")