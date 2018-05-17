""" this file when called in the terminal will merge the trail, report,
and weather dataframes. It also cleans the weathr data"""
import pandas as pd
import numpy as np

#merge all trails together

def merge_trail_files(df_trail,df_report):
    """
    This function left joins trails and reports, adding trail data to the report you built
    **Input parameters**
    ------------------------------------------------------------------------------
    df_trail: pandas df
    df_report: pandas df
    **Output**
    ------------------------------------------------------------------------------
    Merged: Pandas df of reports with added trail information
    """

    # df_reports = df_report.drop('Unnamed: 0',axis =1)
    # df_trails = df_trail.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1)
    merged = pd.merge(df_report, df_trail, left_on='Trail', right_on='hike_name', how='left', sort=False)
    return merged

#to use wheneber reopened as a csv
def change_datetime(df_all):
    """ take the dateframe and turns the Datetime catagory into datetime form"""
    df_all['Datetime'] = df_all['Date'].apply(lambda x: pd.to_datetime(x))
    return df_all



if __name__ == '__main__':
    #import and merge trail info and trail reports
    df_trail = pd.read_csv('../../data/WTA_trails_clean.csv')
    df_report = pd.read_csv('../../data/WTA_olympics_trailreports.csv', sep = '|', lineterminator='\n')
    merged_df = merge_trail_files(df_trail,df_report)
    # df_hike = change_datetime(merged_df)
    # saves merged without weather
    merged_df.to_csv('../../data/olympics_merged.csv', sep = '|')
