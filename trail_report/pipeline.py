'''This file, when run in the terminal, will scrape new data and update the model.'''
from pymongo import MongoClient
import pandas as pd
from webscraping.Webscraping_TrailReports import new_trip_report_builder
from cleaning.Cleaning_TrailReport import clean_trailreport
from cleaning.Merge_dataframes import merge_trail_files
from build_model.make_dataframe import make_split_dataframes
from build_model.make_all_predictions import main_dump

# prep mongo db
mc = MongoClient()
db = mc['wta_all2']
trail_reports = db['trail_reports2']
raw_html = db['html2']
trail_page_raw_html = db['trail_html2']

def update_trip_reports(last_scrape):
    '''scrape new trip reports and add to Mongo db wta_all '''
    # trail_reports.drop()
    # raw_html.drop()
    # trail_page_raw_html.drop()
    hike_urls = pd.read_csv('../../data/WTA_all_trail_data.csv')
    new_trip_report_builder(df,last_scrape)


def clean_trail_reports():
    ''' Transfer trail_reports into pandas df and prep data.'''
    df = pd.DataFrame(list(trail_reports.find()))
    clean__reports_df = clean_trailreport(df)
    return clean__reports_df


def merge_hikes_trail(clean_reports_df):
    ''' Add trail data to each trail; report.'''
    trail_df = pd.read_csv(
        '../../data/WTA_trails_clean.csv',
        sep='|',
        lineterminator='\n')
    merged_df = merge_trail_files(trail_df, clean_reports_df)
    merged_df.to_csv(
        '../../data/WTA_all_merged2.csv',
        sep='|',
        index_label=False)
    return merged_df


def update_dataframe(merged_df):
    '''Split cleaned dataframs for model fitting.'''
    train_X, train_y = make_split_dataframes(merged_df)
    train_X.to_csv('../../data/Xall2.csv', sep='|', index_label=False)
    train_y.to_csv('../../data/yall2.csv', sep='|', index_label=False)


def prep_new_model():
    '''Fit models with updated data.'''
    main_dump()


def update_model(last_scrape):
    '''Update current model with new scraped data.'''
    update_trip_reports(last_scrape)
    clean_reports_df = clean_trail_reports()
    merged_df = merge_hikes_trail(clean_reports_df)
    update_dataframe(merged_df)
    prep_new_model()


if __name__ == '__main__':
    last_scrape = '05/22/18'
    update_model(last_scrape)
