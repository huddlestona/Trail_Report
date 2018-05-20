"""
This file when called in the terminal will merge the trail data
and trail reports and save merged df as a csv.
"""
import pandas as pd
import numpy as np


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
    merged = pd.merge(df_report, df_trail, left_on='Trail', right_on='hike_name', how='left', sort=False)
    return merged

if __name__ == '__main__':
    #import and merge trail info and trail reports
    df_trail = pd.read_csv('../../data/WTA_trails_clean.csv', sep = '|', lineterminator='\n'))
    df_report = pd.read_csv('../../data/WTA_olympics_trailreports.csv', sep = '|', lineterminator='\n')
    merged_df = merge_trail_files(df_trail,df_report)
    merged_df.to_csv('../../data/olympics_merged.csv', sep = '|')
