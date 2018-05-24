import pandas as import pd
import numpy as np

def get_data(merged_df):
    df = pd.from_csv(merged_df)
    all_y =mall_y = df[['Report','condition|snow', 'condition|trail','condition|bugs','condition|road']]
    all_x = df.drop(['Report','condition|snow', 'condition|trail','condition|bugs','condition|road'], axis = 1)
    return all_x,all_y

def pred_x(all_x):
    all_x.drop(['Creator','Trail','_id', 'hike_name','url','super_region'], axis = 1)
    x['month'] = x['Datetime'].apply( lambda x: x.month + x.year)
    x['year'] = x['Datetime'].apply( lambda x: x.year)
    x['monthyear'] = x['Datetime'].apply( lambda x: str(x.month)+'-'+str(x.year))
    month_dum = pd.get_dummies(x['month'])
    year_dum = pd.get_dummies(x['year'])
    monthyear_dummies = pd.get_dummies(x['monthyear'])
    pass_dummies = pd.get_dummies(x['which_pass'])
    subregion_dummies = pd.get_dummies(x['sub_region'])
    all_x = pd.concat([x,monthyear_dummies,subregion_dummies], axis = 1)
    final_x = all_x.drop(['Unnamed: 0','Date_type','month','year','monthyear','sub_region','which_pass','Datetime','last_year','closet_station'], axis=1)
    X = final_x.fillna(0)
    return X

def snow_y(all_y):
    return all_y['condition|snow']

if __name__ == '__main__':
    all_x,all_y = get_data(merged_df)
    X = pred_x(all_x)
    y = snow_y(all_y)
