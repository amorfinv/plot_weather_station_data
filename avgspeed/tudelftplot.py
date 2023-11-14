import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def tudelftplot(config, date_range, plot_data):
    
    # read config
    stations = config['stations']
    column_to_plot = config['column']
    data_path = config['path']

    # get header columns
    header_columns = tudelftheaders(data_path)

    # create the filtered dataframe
    df = tudelftdf(data_path, column_to_plot, date_range, header_columns, stations)

    # get plot data
    plot_data = tudelftplotdata(df, stations, column_to_plot, plot_data)

    return plot_data



def tudelftheaders(data_path):

    header_path = os.path.join(data_path, 'fields.txt')
    # read in the column names,  remove new line characters, and empty spaces
    with open(header_path, 'r') as file:
        columns = file.readlines()
    columns = [column.rstrip('\n') for column in columns]
    columns = [column.split(" ")[-1] for column in columns]

    return columns

def tudelftdf(data_path, column_to_plot, date_range, header_columns, stations):

    # generic arguments for reading csv data
    csv_args = { 
        'on_bad_lines': 'skip',
        'names': header_columns, 
        'na_values': ['NAN'],
        'dtype': {'Albedo': float},
        'comment': '^'
    }

    # create map that combines all dataframes and combine dataframes
    station_paths = [os.path.join(data_path, weather_station + '.csv') for weather_station in stations]
    csv_map = map(lambda file_path: pd.read_csv(file_path, **csv_args), station_paths)
    wind_df = pd.concat(csv_map)

    # Filter data based on date_range
    # convert datetime to datetime object
    wind_df['DateTime'] = pd.to_datetime(wind_df['DateTime'], errors='coerce')

    # Define the desired time range for the year 2022
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    # Filter the wind_data DataFrame to include only dates within the year 2022
    #filtered_wind_df = wind_df.loc['DateTime', start_date:end_date]
    filtered_wind_df = wind_df[(wind_df['DateTime'] >= start_date) & (wind_df['DateTime'] <= end_date)]

    return filtered_wind_df

def tudelftplotdata(df, stations, column_to_plot, plot_data):

    # STEP 4: create log normal fit for each weather station
    for station in stations:
    
        # get station data and the column to plot and remove NaNs 
        station_df = df.loc[df['Name'] == station]
        data_to_fit = station_df[column_to_plot]
        data_to_fit = data_to_fit.dropna()
        data_to_fit = data_to_fit.to_numpy()

        # fit to log normal plot
        shape, loc, scale = stats.lognorm.fit(data_to_fit)
        
        # perform statistical test
        res = stats.kstest(data_to_fit, 'lognorm', args=(shape, loc, scale))

        # create arrays with fit to plot later
        x = np.linspace(data_to_fit.min(), data_to_fit.max(), 100)
        fitted_lognormal = stats.lognorm.pdf(x, shape, loc, scale)

        # save fit parameters
        plot_data[station] = {
                'shape': shape, 
                'loc': loc, 
                'scale': scale, 
                'p': res.pvalue,
                'stat': res.statistic,
                'data': data_to_fit,
                'x_plot': x,
                'y_plot': fitted_lognormal
                }

    return plot_data
