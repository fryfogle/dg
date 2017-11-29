import pandas as pd
import numpy as np
from loop_ivr.outliers.common_functions import *

group_by_list = ['Date', 'Market_Real', 'Crop']
columnlist_ct = ['Date', 'Aggregator', 'Market_Real', 'Crop', 'Quantity_Real', 'Price', 'Amount']

def remove_crop_outliers(ct_data=None):
    daily_aggregator_market_crop_rate_query_result = list(ct_data)

    combined_transactions_data = pd.DataFrame(daily_aggregator_market_crop_rate_query_result)
    combined_transactions_data['Date'] = pd.to_datetime(combined_transactions_data['Date'])

    combined_transactions_data = call_methods(combined_transactions_data)

    combined_transactions_data.to_csv("final_data_after_outliers.csv")

    for recursion_counter in range(0,4):
        combined_transactions_data.fillna(0,inplace=True)
        ct_data = combined_transactions_data[(combined_transactions_data['D/STD'] > 1.3)]
        if ct_data is not None:
            combined_transactions_data = combined_transactions_data[(combined_transactions_data['D/STD'] <= 1.3)]
            combined_transactions_data = combined_transactions_data[columnlist_ct]
            combined_transactions_data = call_methods(combined_transactions_data)
        else:
            break

    # combined_transactions_data = combined_transactions_data[(combined_transactions_data['D/STD'] <= 1.3)]
    # combined_transactions_data = combined_transactions_data[columnlist_ct]
    # combined_transactions_data = call_methods(combined_transactions_data)

    combined_transactions_data.to_csv("final_data_after_outliers_1.csv")
    return combined_transactions_data

def call_methods(combined_transactions_data):
    combined_transactions_data = get_statistics(combined_transactions_data)
    combined_transactions_data = raise_flags(combined_transactions_data)

    combined_transactions_data = combined_transactions_data[(combined_transactions_data['Flag']==1) | (combined_transactions_data['Flag']==5)]

    #Arranging dataframe according to crop, market and date
    combined_transactions_data = combined_transactions_data.groupby(group_by_list).apply(lambda x: x.sort_values(['Crop','Market_Real','Date'],ascending=[True,True,False])).reset_index(drop=True)

    return combined_transactions_data


def get_statistics(combined_transactions_data):

    ct_data_with_mean = combined_transactions_data.groupby(group_by_list).apply(compute_mean).reset_index(name='Av_Rate')
    combined_transactions_data = combined_transactions_data.merge(ct_data_with_mean,how='left',on=group_by_list)

    ct_with_total_quanity = combined_transactions_data.groupby(group_by_list).apply(
        compute_total_q).reset_index(name='Total_Quantity')
    combined_transactions_data = combined_transactions_data.merge(ct_with_total_quanity, how='left',
                                                                  on=group_by_list)

    combined_transactions_data = compute_deviation(combined_transactions_data)

    ct_with_max_deviation = combined_transactions_data.groupby(group_by_list).apply(compute_max_deviation).reset_index(name= 'Max_Deviation')
    combined_transactions_data = combined_transactions_data.merge(ct_with_max_deviation,how='left',on=group_by_list)

    ct_with_std = combined_transactions_data.groupby(group_by_list).apply(compute_std).reset_index(name= 'STD')
    combined_transactions_data = combined_transactions_data.merge(ct_with_std,how='left',on=group_by_list)

    combined_transactions_data = compute_ratios(combined_transactions_data)
    return combined_transactions_data


# Flag = 0: Untouched
# Flag = 1: Okay
# Flag = 2: MI Outlier
# Flag = 3: Incorrect data. Ask admin
# Flag = 4: No clue. Try other method. Don't send to MI.
# Flag = 5: Iterate.

def raise_flags(combined_transactions_data):
    # All STD should get replaced by STD/Mean and/or D/Mean
    # For STD< 1, still find Flag #3 by checking D/Mean ratio?
    combined_transactions_data.loc[combined_transactions_data['STD'] <= 1, 'Flag'] = 1

    combined_transactions_data.loc[
        (combined_transactions_data['STD'] <= 2) & (combined_transactions_data['STD'] > 1) & (
            combined_transactions_data['Max_Deviation'] / combined_transactions_data['STD'] > 1.3), 'Flag'] = 5
    combined_transactions_data.loc[
        (combined_transactions_data['STD'] <= 2) & (combined_transactions_data['STD'] > 1) & (
            combined_transactions_data['Max_Deviation'] / combined_transactions_data['STD'] > 1) & (
            combined_transactions_data['Max_Deviation'] / combined_transactions_data['STD'] <= 1.3) & (combined_transactions_data['Deviation_Factor'] > 0.5), 'Flag'] = 2
    combined_transactions_data.loc[
        (combined_transactions_data['STD'] <= 2) & (combined_transactions_data['STD'] > 1) & (
            combined_transactions_data['Max_Deviation'] / combined_transactions_data['STD'] > 1) & (
            combined_transactions_data['Max_Deviation'] / combined_transactions_data['STD'] <= 1.3) & (
        combined_transactions_data['Deviation_Factor'] <= 0.5), 'Flag'] = 1
    combined_transactions_data.loc[
        (combined_transactions_data['STD'] <= 2) & (combined_transactions_data['STD'] > 1) & (
            combined_transactions_data['Max_Deviation'] / combined_transactions_data['STD'] <= 1), 'Flag'] = 1

    combined_transactions_data.loc[(combined_transactions_data['STD'] <= 3) & (combined_transactions_data['STD'] > 2) & (
        combined_transactions_data['Max_Deviation']/combined_transactions_data['STD'] <= 1.3), 'Flag'] = 4
    combined_transactions_data.loc[
        (combined_transactions_data['STD'] <= 3) & (combined_transactions_data['STD'] > 2) & (
            combined_transactions_data['Max_Deviation'] / combined_transactions_data['STD'] > 1.3), 'Flag'] = 5

    combined_transactions_data.loc[(combined_transactions_data['STD'] > 3) & (combined_transactions_data['STD'] <= 6.5) & (combined_transactions_data['Max_Deviation']/combined_transactions_data['STD'] > 1.3), 'Flag'] = 5
    combined_transactions_data.loc[
        (combined_transactions_data['STD'] > 3) & (combined_transactions_data['STD'] <= 6.5) & (
        combined_transactions_data['Max_Deviation'] / combined_transactions_data['STD'] <= 1.3), 'Flag'] = 4

    combined_transactions_data.loc[
        (combined_transactions_data['STD'] > 6.5) & (combined_transactions_data['STD'] <= 9) & (
        combined_transactions_data['Max_Deviation'] / combined_transactions_data['STD'] > 1.3), 'Flag'] = 5
    combined_transactions_data.loc[
        (combined_transactions_data['STD'] > 6.5) & (combined_transactions_data['STD'] <= 9) & (
            combined_transactions_data['Max_Deviation'] / combined_transactions_data['STD'] <= 1.3), 'Flag'] = 4

    combined_transactions_data.loc[(combined_transactions_data['STD'] > 9), 'Flag'] = 4
    # combined_transactions_data.to_csv("check_5.csv")
    return combined_transactions_data
