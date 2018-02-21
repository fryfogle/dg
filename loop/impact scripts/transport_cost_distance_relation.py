import pandas as pd

import Tables
import Transport_Cost


def get_cost_distance():
    # List of state-wise frequently used vehicles
    vehicles_to_fill_na_data = {'State': [1,1,1,1,1], 'Vehicle_ID': [0, 2, 3, 4, 5]}
    vehicles_to_fill_na = pd.DataFrame(data= vehicles_to_fill_na_data)

    # columnlist = ['Date', 'Aggregator', 'Market', 'DT_ID', 'Vehicle_ID', 'Vehicle_Name','Transport_Cost','Quantity', 'State' ]
    daily_transportation_data = Tables.daily_transportation_data

    # aggregator_market_vehicle_predicted_cost_quantity = Transport_Cost.get_transport_cost_amv(daily_transportation_data, vehicles_to_fill_na)
    #
    # a_m_v_cost_bihar = aggregator_market_vehicle_predicted_cost_quantity[aggregator_market_vehicle_predicted_cost_quantity['State']==1]
    # print aggregator_market_vehicle_predicted_cost_quantity.count()
    # print a_m_v_cost_bihar.count()

    daily_vehicle_single_data = Transport_Cost.get_single_vehicle_data(daily_transportation_data)
    daily_vehicle_single_data = daily_vehicle_single_data[daily_vehicle_single_data['State']==1]

    vehicle_quantity_limits = Transport_Cost.find_vehicle_quantity_limits(daily_vehicle_single_data)

    aggregator_market_vehicle_cost_detailed = Transport_Cost.find_transport_cost_amv(daily_vehicle_single_data, vehicle_quantity_limits)

    aggregator_market_vehicle_cost = aggregator_market_vehicle_cost_detailed.drop(
        ['Quantity_Min', 'Quantity_Limit'], axis=1) #'Vehicle_Name',

    # print aggregator_market_vehicle_cost.head(n=10)

    df_distance = pd.read_csv('mandi_village_mapping.csv')
    df_distance.drop(['Unnamed: 0','loop_user__id','mandi__latitude','mandi__longitude','village__latitude','village__longitude', 'village__village_name_en', 'village__id'], axis = 1,inplace = True)
    df_distance.rename(columns={"loop_user__user__id":"Aggregator","mandi__id":"Market"},inplace=True)

    # print df_distance.head()

    cost_distance_vehicle = pd.merge(aggregator_market_vehicle_cost,df_distance, on=['Aggregator','Market'],how="inner")
    cost_distance_vehicle['distance_km'] = cost_distance_vehicle['distance'].str.split(' ').str[0].astype('float64')
    cost_distance_vehicle['cost_per_km'] = cost_distance_vehicle['Predicted_TC'] / cost_distance_vehicle['distance_km']
    print cost_distance_vehicle.head(n=25)




if __name__=="__main__":
    get_cost_distance()
