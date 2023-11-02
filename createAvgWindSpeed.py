import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
from functions import fixPlot

# configuration
weather_stations = ['Oost', 'Ommoord', 'Bolnes', 'SpaansePolder', 'Ridderkerk', 'Heijplaat', 'Delfshaven']
column_to_plot = 'WindSpd_{Avg}'
range_to_plot = ['2022-01-01','2022-12-31']
figx, figy = 10, 8

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
fit_parameters = {}
for weather_station in weather_stations:
   
   # get station data and the column to plot and remove NaNs 
   station_df = filtered_wind_df.loc[filtered_wind_df['Name'] == weather_station]
   data_to_fit = station_df[column_to_plot]
   data_to_fit = data_to_fit.dropna()

   # fit to log normal plot
   shape, loc, scale = stats.lognorm.fit(data_to_fit)
   
   # perform statistical test
   res = stats.kstest(data_to_fit, 'lognorm', args=(shape, loc, scale))

   # create arrays with fit to plot later
   x = np.linspace(data_to_fit.min(), data_to_fit.max(), 100)
   fitted_lognormal = stats.lognorm.pdf(x, shape, loc, scale)

   # save fit parameters
   fit_parameters[weather_station] = {
           'shape': shape, 
           'loc': loc, 
           'scale': scale, 
           'p': res.pvalue,
           'stat': res.statistic,
           'data': data_to_fit,
           'x_plot': x,
           'y_plot': fitted_lognormal
           }


# STEP 5: create plots

if os.path.exists("images") and os.path.isdir("images"):
    print("Generating the plots....") 
else:
    print("Creating images/ folder....")
    os.makedirs("images")

# create individual plots for each weather_station comparing it to
for weather_station, fit_dict in fit_parameters.items():
    
    # get the plot title from configuration
    plot_title = plot_titles[column_to_plot]

    # get filename
    filename = '_'.join([weather_station, plot_title, *range_to_plot]) + '.png'
    filename = filename.replace(" ", "").lower()
    
    # get the x axis name depending on what is being plotted    
    x_axis_label = 'Wind Speed (m/s)' if 'speed' in filename else 'Wind Direction (degrees)'

    # start plot
    fixPlot(thickness=1.5, fontsize=25, markersize=8, labelsize=20, texuse=True, tickSize = 15)
    plt.figure(figsize=(figx,figy))
    plt.hist(fit_dict['data'], bins='auto', density=True, label='Weather station data')
    plt.plot(fit_dict['x_plot'], fit_dict['y_plot'], 'r-', label='Fitted Log-normal Distribution')
    plt.xlabel(x_axis_label)
    plt.ylabel('Probability density function')
    plt.legend(frameon=False)    
    plt.title(f'PDF of {plot_title} for {weather_station} weather station \n from {range_to_plot[0]} to {range_to_plot[1]}')
    plt.savefig(os.path.join('images', filename))
    plt.close()

# crete combined plots

fixPlot(thickness=1.5, fontsize=25, markersize=8, labelsize=20, texuse=True, tickSize = 15)
plt.figure(figsize=(figx,figy))

# get the plot title from configuration and xlabel
plot_title = plot_titles[column_to_plot]
x_axis_label = 'Wind Speed (m/s)' if 'speed' in plot_title else 'Wind Direction (degrees)'

filename = '_'.join(['stationcomparison', plot_title, *range_to_plot]) + '.png'
filename = filename.replace(" ", "").lower()

for weather_station, fit_dict in fit_parameters.items():
    plt.plot(fit_dict['x_plot'], fit_dict['y_plot'], label=weather_station)

plt.xlabel(x_axis_label)
plt.ylabel('Probability density function')
plt.legend(frameon=False)
plt.title(f'Log-normal comparisions of {plot_title} \n from {range_to_plot[0]} to {range_to_plot[1]}')
plt.savefig(os.path.join('images', filename))
plt.close()

