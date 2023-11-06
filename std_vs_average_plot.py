import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

# configuration
weather_stations = ['Oost', 'Ommoord', 'Bolnes', 'SpaansePolder', 'Ridderkerk', 'Heijplaat', 'Delfshaven']
range_to_plot = ['2022-01-01','2022-12-31']

plot_titles = {
        'WindSpd_{Avg}': 'Average wind speeds',
        'WindSpd_{Max}': 'Maximum wind speeds'
        }

data_dir = 'data'
# STEP 1: read in the column names from fields.txt

# read in the column names,  remove new line characters, and empty spaces
with open('data/fields.txt', 'r') as file:
   columns = file.readlines()
columns = [column.rstrip('\n') for column in columns]
columns = [column.split(" ")[-1] for column in columns]


# STEP 2: read csv to a dataframe

# generic arguments for reading csv data
csv_args = { 
    'on_bad_lines': 'skip',
    'names': columns, 
    'na_values': ['NAN'],
    'dtype': {'Albedo': float},
    'comment': '^'
}

# create map that combines all dataframes and combine dataframes
weather_station_paths = [os.path.join(data_dir, weather_station + '.csv') for weather_station in weather_stations]
csv_map = map(lambda file_path: pd.read_csv(file_path, **csv_args), weather_station_paths)
wind_df = pd.concat(csv_map)

# STEP 3: Filter data based on date_range

# convert datetime to datetime object
wind_df['DateTime'] = pd.to_datetime(wind_df['DateTime'], errors='coerce')

# Define the desired time range for the year 2022
start_date = pd.to_datetime(range_to_plot[0])
end_date = pd.to_datetime(range_to_plot[1])

# Filter the wind_data DataFrame to include only dates within the year 2022
#filtered_wind_df = wind_df.loc['DateTime', start_date:end_date]
filtered_wind_df = wind_df[(wind_df['DateTime'] >= start_date) & (wind_df['DateTime'] <= end_date)]


# STEP 4: create log normal fit for each weather station

avg_speed_column = 'WindSpd_{Avg}'
std_speed_column = 'WindSpd_{Std}'

for weather_station in weather_stations:
   
   # get station data and the column to plot and remove NaNs 
   station_df = filtered_wind_df.loc[filtered_wind_df['Name'] == weather_station]
   data_to_fit = station_df[[avg_speed_column, std_speed_column]].dropna()

   # start plot
   plt.figure()
   plt.scatter(data_to_fit[avg_speed_column],data_to_fit[std_speed_column], label='Weather station data')
   plt.xlabel('Average speed (m/s)')
   plt.ylabel('Standard deviation (m/s)')
   #plt.legend()    
   plt.title(f'{weather_station} weather station \n from {range_to_plot[0]} to {range_to_plot[1]}')
   #plt.savefig(os.path.join('images', filename))
   plt.show()


